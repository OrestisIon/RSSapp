// Create a ViewFeed component that will display entries of the feed.
// It will take the feed as a prop and call the API to fetch the entries. 
// The entries will be displayed in a list with the title, date, and URL.
import React, { useState, useEffect } from 'react';
import { apiCall } from 'lib/util';
import { useLocation, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import DashboardLayout from 'examples/LayoutContainers/DashboardLayout';

const ViewFeed = () => {
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const [entries, setEntries] = useState([]);
    const [total, setTotal] = useState([]);
    const { pathname } = useLocation();
    const location = useLocation();
    const data = location.state;
    useEffect(() => {
        //check if the data is type of object feed
        if (typeof data !== 'object' || !Object.prototype.hasOwnProperty.call(data, 'id') || !Object.prototype.hasOwnProperty.call(data, 'title')) {
            setEntries([]);
            setTotal([]);
            navigate('/MyFeeds');
            return;
        }
        const fetchEntries = async () => {
            try {
                const e = await apiCall(`feeds/${data.id}/entries?limit=1&order=published_at&direction=asc`, setError);
                console.log(e);
                setTotal(e.total);
                if(e.total > 0)
                    setEntries(e.entries);
            } catch (err) {
                setError(err);
            }
        };

        fetchEntries();
    }, [data.id, setError, setEntries]);


    return (
        <DashboardLayout>
            {total > 0 ? (
            <div>
            <h1>{data.title}</h1>
            <ul>
                {entries.map((entry, i) => (
                    <li key={i}>
                        <a href={entry.url} target="_blank" rel="noreferrer">{entry.title}</a>
                        <p>{entry.published}</p>
                    </li>
                ))}
            </ul>
            </div> ) : (
                    <h2>Feed {data.title} has no entries</h2>
            )}

        </DashboardLayout>
    );
}
export default ViewFeed;