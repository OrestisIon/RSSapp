
// @mui material components
import Grid from "@mui/material/Grid";
import * as React from 'react';
// Material Dashboard 2 React components
import MDBox from "components/MDBox";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import { useState, useEffect } from "react";
import Divider from '@mui/material/Divider';

// react-router-dom components
import { Link } from "react-router-dom";
import MDAlert from "components/MDAlert";

// @mui material components
import Card from "@mui/material/Card";
import Switch from "@mui/material/Switch";
import { Typography, Container } from '@mui/material';
import { apiCall } from "lib/util";

// Material Dashboard 2 React components
import MDTypography from "components/MDTypography";
import MDInput from "components/MDInput";
import MDButton from "components/MDButton";
import FeedGrid from "components/FeedGrid";
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
const PREFIX = 'FORYOU';
import { styled } from '@mui/system';

const classes = {
    root: `${PREFIX}-root`,
    card: `${PREFIX}-card`,
    media: `${PREFIX}-media`,
};

const StyledContainer = styled(Container)(({ theme }) => ({
    [`&.${classes.root}`]: {
        flexGrow: 1,
    },

    [`& .${classes.card}`]: {
        marginBottom: theme.spacing(2),
    },

    [`& .${classes.media}`]: {
        height: 140,
    },
}));

function Reccom() {
    const [feedurl, setFeedurl] = useState('');
    const [password, setPassword] = useState('');
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState('');
    const [alignment, setAlignment] = React.useState('web');
    const [loading, setLoading] = useState(false);
    const [dataA, setDataA] = useState([]);
    const [dataB, setDataB] = useState([
        {
            "generalTitle": "Feed Title 1",
            "blogs": [
                { "title": "Blog 1-1", "description": "Description 1-1" },
                { "title": "Blog 1-2", "description": "Description 1-2" }
            ]
        },
        {
            "generalTitle": "Feed Title 2",
            "blogs": [
                { "title": "Blog 2-1", "description": "Description 2-1" },
                { "title": "Blog 2-2", "description": "Description 2-2" }
            ]
        }
    ]);

    const handleAlChange = (event, newAlignment) => {
        setAlignment(newAlignment);
    };

    
    // Handle change in input fields
    const handleChange = (event) => {
        const { name, value } = event.target;
        // Reset validation messages on input change

        if (name === 'feedurl') setFeedurl(value);
    };

 
    const fetchFeeds = async () => {
        try {
            setLoading(true);
            const f = await apiCall('get_feed_recommendations', setError);
            setDataA(f);
        } catch (error) {
            console.error('Error fetching feeds:', error);
            setError(error);
        }
        finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFeeds();
    }, []);



    const [currentData, setCurrentData] = useState(dataA);

    return (
        <DashboardLayout>
            <div>
                < StyledContainer className={classes.root} >
                 
            
            <Grid spacing={1} p={10} direction="column" justifyContent="center" alignItems="center" marginTop={0}>
                        <Grid item mb={7}>

                        <Typography variant="h4" gutterBottom>
                            Today
                        </Typography>
                        <Typography variant="subtitle1" gutterBottom>
                            The insights you need to keep ahead
                            </Typography>
                        </Grid>
                   
                        <Grid item mb={3}>
                        <ToggleButtonGroup
                            sx={{
                                opacity: 1, borderRadius: 2, boxShadow: 1, marginBottom: -1, marginTop: 2, fontWeight: 'bold'}}
                            color="info"
                            value={alignment}
                            exclusive
                            onChange={handleAlChange}
                            aria-label="Platform"
                            size="large"
                            
                        >
                            <ToggleButton value="web" sx={{ fontWeight: 'bold' }} onClick={() => setCurrentData(dataA)}>Based on your subscriptions</ToggleButton>
                            <ToggleButton value="android" sx={{ fontWeight: 'bold' }} onClick={() => setCurrentData(dataB)}>Based on your favourites</ToggleButton>
                        </ToggleButtonGroup>
                        <Divider sx={{ color: 'blue' }} orientation="horizontal" variant="fullWidth" />


                    </Grid>
                    {currentData.map((feed, index) => (
                    <Grid  key={index} >
                            <FeedGrid gridTitle={feed.generalTitle} blogs={feed.blogs} />
                    </Grid>
                ))}
                    </Grid>
                </StyledContainer >

            </div>
        </DashboardLayout>
        
    );
}

export default Reccom;