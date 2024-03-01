// Create a ViewFeed component that will display entries of the feed.
// It will take the feed as a prop and call the API to fetch the entries. 
// The entries will be displayed in a list with the title, date, and URL.
import React, { useState, useEffect } from 'react';
import { apiCall } from 'lib/util';
import { useLocation, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import DashboardLayout from 'examples/LayoutContainers/DashboardLayout';
import { MDBContainer, MDBRow, MDBCol, MDBRipple, MDBBtn } from 'mdb-react-ui-kit';
const ViewFeed = () => {
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const [entries, setEntries] = useState([]);
    const [total, setTotal] = useState([]);
    const [refreshing, setRefreshing] = useState(false);
    const [loading, setLoading] = useState(true);
    const { pathname } = useLocation();

    const location = useLocation();
    const data = location.state;
    useEffect(() => {
        setLoading(true);
        //check if the data is type of object feed
        if (typeof data !== 'object' || !Object.prototype.hasOwnProperty.call(data, 'id') || !Object.prototype.hasOwnProperty.call(data, 'title')) {
            setEntries([]);
            setTotal([]);
            navigate('/ForYou');
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
            finally {
                setLoading(false);
            }

        };

        fetchEntries();
    }, [data.id, setError, setEntries]);

    const onRefresh = async () => {
        setRefreshing(true);
        try {
            await fetchNews();
        } finally {
            setRefreshing(false);
        }
    };


    return (
        <DashboardLayout>
            {total > 0 ? (
                <MDBContainer className="py-5">
                    <MDBRow className="gx-5">
                        <MDBCol md="6" className="mb-4">
                            <MDBRipple
                                className="bg-image hover-overlay ripple shadow-2-strong rounded-5"
                                rippleTag="div"
                                rippleColor="light"
                            >
                                {/* <img
                                    src="https://mdbcdn.b-cdn.net/img/new/slides/080.webp"
                                    className="w-100"
                                /> */}
                                <a href="#!">
                                    <div
                                        className="mask"
                                        style={{ backgroundColor: "rgba(251, 251, 251, 0.15)" }}
                                    ></div>
                                </a>
                            </MDBRipple>
                        </MDBCol>
                        <MDBCol md="6" className="mb-4">
                            <span className="badge bg-danger px-2 py-1 shadow-1-strong mb-3">
                              
                            </span>
                            <h4>
                                <strong>Facilis consequatur eligendi</strong>
                            </h4>
                            <p className="text-muted">
                                Lorem ipsum dolor sit amet consectetur adipisicing elit. Facilis
                                consequatur eligendi quisquam doloremque vero ex debitis veritatis
                                placeat unde animi laborum sapiente illo possimus, commodi
                                dignissimos obcaecati illum maiores corporis.
                            </p>
                            <MDBBtn>Read More</MDBBtn>
                        </MDBCol>
                            

                    </MDBRow>
                </MDBContainer>

            // <div>
            // <h1>{data.title}</h1>
            // <ul>
            //     {entries.map((entry, i) => (
            //         <li key={i}>
            //             <a href={entry.url} target="_blank" rel="noreferrer">{entry.title}</a>
            //             <p>{entry.published}</p>
            //         </li>
            //     ))}
            // </ul>
            // </div> ) 
            ):(
                    <h2>Feed {data.title} has no entries</h2>
            )}
                            

        </DashboardLayout>
    );
}
export default ViewFeed;