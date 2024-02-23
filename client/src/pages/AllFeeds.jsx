
import React, { useState, useEffect } from 'react'
import {Allotment} from 'allotment'
import FeedBrowser from './FeedBrowser'
import ItemBrowser from './ItemBrowser'
import ItemViewer from 'pages/ItemViewer'
import { KeyHelpModal, SettingsModal } from './Modals'
import styled from 'styled-components'
import { useHotkeys } from 'react-hotkeys-hook'
import { apiCall, createFeedIcon } from 'lib/util'
import ClickNHold from 'react-click-n-hold'
// Material Dashboard 2 React context
import { useMaterialUIController } from "context";
// react-router-dom components
import { useLocation } from "react-router-dom";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";



const ErrorDiv = styled.div`
	padding: 10px;
	background-color: ${(props) => props.theme.errorbg};
	color: ${(props) => props.theme.errorfg};
	text-align: center;
	position: absolute;
	width: 100%;
	z-index: 100;
	font-weight: bold;
`

const ErrorClose = styled.div`
	float: right;
	margin-right: 20px;
`

const FloatingButton = styled.button`
	float: right;
	margin-top: 5px;
	margin-right: 5px;
	font-size: 16px;
	width: 30px;
	height: 30px;
`

const sum = (arr) => {
    return arr.reduce((a, b) => {
        return a + (b['unreads'] || 0)
    }, 0)
}


function AllFeeds() {
    const [controller, dispatch] = useMaterialUIController();
    const { miniSidenav } = controller;
    const { pathname } = useLocation();

    const [error, setError] = useState()
    const [currentFeed, setCurrentFeed] = useState()
    const [currentItem, setCurrentItem] = useState()
    const [feeds, setFeeds] = useState([])

    const [helpOpen, setHelpOpen] = useState(false)

    const [updateFeedsTrigger, setUpdateFeedsTrigger] = useState(true)
    const [renderFeedsTrigger, setRenderFeedsTrigger] = useState(true)
    const [updateUnreadTrigger, setUpdateUnreadTrigger] = useState([])

    const [, updateState] = React.useState()
    const forceUpdate = React.useCallback(() => updateState({}), [])

    const cache = JSON.parse(localStorage.getItem('favicons')) || {}

    useEffect(() => {
        localStorage.setItem('refresh', 60)
        const fetchFeeds = async () => {
            const f = await apiCall('feeds', setError)
            let categories = []
            f.forEach((x) => {
                if (!categories.find((c) => c.id === x.category.id))
                    categories.push(x.category)
            })

            const feedTree = [
                { id: -1, title: 'All', fetch_url: 'entries', unreads: 0 },
                {
                    id: -2,
                    title: 'Starred',
                    fetch_url: 'entries?starred=true',
                    unreads: 0,
                },
            ]

            categories
                .filter((f) => f)
                .sort((a, b) => a.title.localeCompare(b.title))
                .forEach((c) => {
                    feedTree.push(c)
                    feedTree.push(
                        ...f
                            .filter((f) => f.category.id === c.id)
                            .sort((a, b) => a.title.localeCompare(b.title))
                            .map((f) =>
                                Object.assign(f, {
                                    fetch_url: 'feeds/' + f.id + '/entries',
                                    is_feed: true,
                                })
                            )
                    )
                })

            feedTree.forEach(async (f) => {
                f.icon_data = createFeedIcon(f.title)
                if (f.icon && f.id in cache) {
                    f.icon_data = cache[f.id]
                } else if (f.icon) {
                    try {
                        const icon = await apiCall(
                            'feeds/' + f.id + '/icon',
                            (e) => { }
                        )
                        f.icon_data = 'data:' + icon.data
                    } catch { }

                    localStorage.setItem(
                        'favicons',
                        JSON.stringify({
                            ...JSON.parse(localStorage.getItem('favicons')),
                            [f.id]: f.icon_data,
                        })
                    )
                    forceUpdate()
                }
            })
            setFeeds(feedTree)
            setUpdateUnreadTrigger(feedTree)
        }
        if (updateFeedsTrigger) fetchFeeds()
        setUpdateFeedsTrigger(false)
    }, [updateFeedsTrigger, cache, forceUpdate])

    useEffect(() => {
        if (localStorage.getItem('refresh') > 0) {
            let timer = setInterval(
                () => setUpdateFeedsTrigger(true),
                1000 * localStorage.getItem('refresh')
            )
            return () => clearInterval(timer)
        }
        // eslint-disable-next-line
    }, [localStorage.getItem('refresh')])

    useEffect(() => {
        const updateUnread = async (f, state) => {
            if (parseInt(f)) {
                state = feeds
                f = feeds.find((x) => x.id === f && x.fetch_url)
            }
            if (!f.fetch_url) return

            const unread = await apiCall(
                f.fetch_url +
                (f.fetch_url.includes('?') ? '&' : '?') +
                'status=unread&limit=1',
                setError
            )
            f['unreads'] = unread.total
            setRenderFeedsTrigger(true)

            document.title =
                sum(state.filter((f) => f.id > 0 && f.is_feed)) +
                ' | reminiflux'

            state
                .filter((f) => !f.fetch_url)
                .forEach((c) => {
                    c['unreads'] = sum(
                        state.filter(
                            (x) => x.category && x.category.id === c.id
                        )
                    )
                })

            forceUpdate()
        }

        if (updateUnreadTrigger.length > 0) {
            ;[-2, -1, ...updateUnreadTrigger].forEach((u) =>
                updateUnread(u, updateUnreadTrigger)
            )
            setUpdateUnreadTrigger([])
        }
    }, [feeds, forceUpdate, updateUnreadTrigger])

    const markAllRead = async (f) => {
        const urls = f.fetch_url
            ? [f.fetch_url]
            : feeds
                .filter((x) => x.category)
                .filter((x) => x.category.id === f.id)
                .map((x) => x.fetch_url)

        const result = await Promise.all(
            urls.map(
                (u) =>
                    apiCall(
                        u + (u.includes('?') ? '&' : '?') + '&status=unread'
                    ),
                setError
            )
        )

        const items = []
        result.forEach((i) => items.push(...i.entries))

        if (!items.length) return

        await apiCall('entries', setError, {
            entry_ids: items.map((x) => x.id),
            status: 'read',
        })

        setUpdateUnreadTrigger(
            items
                .map((x) => x.feed.id)
                .filter((f, index, self) => self.indexOf(f) === index)
        )
    }

    const refreshFeedCounts = () => {
        setUpdateUnreadTrigger(feeds.map((x) => x.id))
    }
    const refreshFeeds = async () => {
        await apiCall('feeds/refresh', setError, {})
        setUpdateFeedsTrigger(true)
    }

    // useHotkeys(
    //     'shift+d',
    //     () => {
    //          setTheme(theme === 'light' ? 'dark' : 'light')
    //     },
    //     [settingsOpen, theme]
    // )

    useHotkeys(
        'r',
        () => {
            refreshFeedCounts()
        },
        [feeds]
    )
    useHotkeys(
        'shift+r',
        () => {
            refreshFeeds()
        },
        [feeds]
    )

    return (
        // <div style={{ display: 'flex', justifyContent: 'center', height: '100vh' }}>

        <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh',
            overflow: 'auto'
        }}>
            <MDBox
                sx={({ breakpoints, transitions, functions: { pxToRem } }) => ({
                    p: 20,
                    position: "relative",
                    maxWidth: "calc(100% - 200px)", // Assuming 200px is the expanded sidenav width, adjust as needed
                    width: "150%", // Ensures MDBox takes the full width of its container, respecting maxWidth
                    boxSizing: 'border-box', // Ensures padding is included in the width calculation
                    marginLeft: miniSidenav ? pxToRem(600) : pxToRem(600), // Adjust marginLeft based on miniSidenav state
                    transition: transitions.create(["margin-left", "margin-right"], {
                        easing: transitions.easing.easeInOut,
                        duration: transitions.duration.standard,
                    }),
                    [breakpoints.up("xl")]: {
                        marginLeft: miniSidenav ? pxToRem(120) : pxToRem(700), // Ensures consistent marginLeft adjustment for "xl" breakpoints
                    },
                })}
            >
            {
                <Allotment vertical style={{ width: '100%' }}>
                    <Allotment.Pane
                        minSize={250}
                        preferredSize={parseInt(localStorage.getItem('v_split')) || '35%'}
                        onSizeChange={(size) => localStorage.setItem('v_split', size.toString())}>
                        <div>
                            <ClickNHold
                                time={2}
                                onClickNHold={refreshFeeds}
                                onEnd={(e, enough) => {
                                    if (!enough) refreshFeedCounts();
                                    e.target.blur();
                                }}>
                                <FloatingButton
                                    title="Short press to refresh unread count, long press to trigger fetch and full refresh">
                                    &#8635;
                                </FloatingButton>
                            </ClickNHold>
                            <FeedBrowser
                                currentFeed={currentFeed}
                                feeds={feeds}
                                onFeedChange={setCurrentFeed}
                                markAllRead={markAllRead}
                                errorHandler={setError}
                                updateTrigger={renderFeedsTrigger}
                                clearTrigger={setRenderFeedsTrigger}
                            />
                        </div>
                    </Allotment.Pane>
                    <Allotment.Pane
                        preferredSize={parseInt(localStorage.getItem('h_split')) || '40%'}
                        onSizeChange={(size) => localStorage.setItem('h_split', size.toString())}>
                        <Allotment>
                            <Allotment.Pane minSize="10%">
                                <ItemBrowser
                                    currentFeed={currentFeed}
                                    currentItem={currentItem}
                                    feeds={feeds}
                                    onItemChange={setCurrentItem}
                                    updateUnread={setUpdateUnreadTrigger}
                                    errorHandler={setError}
                                />
                            </Allotment.Pane>
                            <Allotment.Pane>
                                <ItemViewer
                                    currentItem={currentItem}
                                    onFeedChange={(f) => setCurrentFeed(feeds.find((i) => i.id === f.id))}
                                    errorHandler={setError}
                                />
                            </Allotment.Pane>
                        </Allotment>
                    </Allotment.Pane>
                </Allotment>
            }
            </MDBox >
     </div>
    );
}

export default AllFeeds;