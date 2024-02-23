import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardMedia, Typography, Grid, Container } from '@mui/material';
import { styled } from '@mui/system';
import { apiCall } from 'lib/util';
const PREFIX = 'FORYOU';

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
    // Assuming the sum function is used only in this component
    const sum = (arr) => {
        return arr.reduce((a, b) => {
            return a + (b['unreads'] || 0);
        }, 0);
    };
function ForYou() {
    // const { pathname } = useLocation();
    const [error, setError] = useState(null);
    const [feeds, setFeeds] = useState([]);
    // const [, updateState] = React.useState();
    // const forceUpdate = useCallback(() => updateState({}), []);

    const fetchFeeds = async () => {
        try {
          const f = await apiCall('feeds', setError)
            let categories = f.map(feed => feed.category).filter((v, i, a) => a.indexOf(v) === i); // Unique categories

            let feedTree = [
                { id: -1, title: 'All', fetch_url: 'entries', unreads: 0 },
                { id: -2, title: 'Starred', fetch_url: 'entries?starred=true', unreads: 0 },
                // Add categories and feeds to feedTree...
            ];
          console.log(feedTree)
          console.log(f)
          console.log(JSON.stringify(f))   
            // Add feeds to categories...
            // Omitted for brevity

            // Update state with the feed tree
            setFeeds(f);
        } catch (error) {
            console.error('Error fetching feeds:', error);
            setError(error);
        }
    };

    useEffect(() => {
        fetchFeeds();
    }, []);

    return (
        < StyledContainer className = { classes.root } >
      <Typography variant="h4" gutterBottom>
        Today
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        The insights you need to keep ahead
      </Typography>
      <Grid container spacing={2}>
        {feeds.map((feed, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card className={classes.card}>
              {feed.icon && (
                <CardMedia
                  className={classes.media}
                  image={feed.icon}
                  title={feed.title}
                />
              )}
              <CardContent>
                <Typography variant="h5" component="h2">
                  {feed.title}
                </Typography>
                <Typography variant="body2" color="textSecondary" component="p">
                  {feed.feed_url}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </StyledContainer >
    );
}

export default ForYou;