// @mui material components
import Grid from "@mui/material/Grid";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import { useState } from "react";

// react-router-dom components
import { Link } from "react-router-dom";
import MDAlert from "components/MDAlert";

// @mui material components
import Card from "@mui/material/Card";
import Switch from "@mui/material/Switch";

// Material Dashboard 2 React components
import MDTypography from "components/MDTypography";
import MDInput from "components/MDInput";
import MDButton from "components/MDButton";
import { postRequest } from "lib/util"; 
function AddFeed() {
    const [feedurl, setFeedurl] = useState('');
    const [password, setPassword] = useState('');
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState('');

    // Handle change in input fields
    const handleChange = (event) => {
        const { name, value } = event.target;
        // Reset validation messages on input change

        if (name === 'feedurl') setFeedurl(value);
    };

    // Other component logic remains the same
    const handleSubmit = async (event) => {
        event.preventDefault();
        let isValid = true;
        let messages = { url: '' };
        if (feedurl.length < 3) {
            messages.url = 'Url must be non-empty.';
            isValid = false;
        }
        if (isValid) {
            console.log('Adding Feed...');
            try {
                await postRequest('feeds', { url: feedurl }, error);
            } catch (err) {
                // Handle login failure (e.g., invalid credentials)
                setError('Failed to log in. Please check your credentials.');
            }
        }
    };

    return (
        <DashboardLayout>
            <Grid container={true} spacing={1} direction="column" 
                alignItems="center">
                <MDBox flexDirection='column' width="80%" alignItems='center' justifyContent='center'  py={6}>
                    <Card>
                        <MDBox
                        variant="gradient"
                        bgColor="transparent"
                        borderRadius="lg"
                        coloredShadow="INFO"
                        opacity={1}
                        mx={30}
                        mt={2}
                        p={4}
                        mb={6}
                            textAlign="center"
                            sx={{ whiteSpace: 'nowrap' }}
                    >
                        <MDTypography variant="h2" textGradient="true" fontWeight="medium" color="dark" mt={1}>
                            Add New Feed
                        </MDTypography>
                        </MDBox >
                        <MDBox component="form" role="form" onSubmit={handleSubmit}>
                        <MDBox alignItems='center' textAlign="center" mx={30} p={4} mb={1} display="flex" justifyContent="center">
                                <MDInput sx={{ textAlign: "center", width: "80%" }} type="url" label="Feed URL" onChange={handleChange} size="large"  />
                        </MDBox>

                        <MDBox alignItems='center' textAlign="center" mx={30} p={4} mb={3} display="flex" justifyContent="center">
                            <MDButton sx={{ textAlign:"center", width: "40%"}} size="large" type="submit" variant="gradient" color="info">
                                Press to Add
                            </MDButton>
                            </MDBox>
                        </MDBox>
                            {/* Display error message at the top of the form */}
                            
                        <MDBox lignItems='center' textAlign="center" mx={50}  display="flex" justifyContent="center">
                            <MDTypography sx={{ textAlign: "center", width: "100%" }} variant="button" color="text">
                                {error && (
                                    <MDAlert textAlign="center" color="error">
                                        <MDTypography textAlign="center" fontWeight="bold" color="white">Failed to add Feed</MDTypography>
                                    </MDAlert>
                                )}
                                {success && (
                                <MDAlert  textAlign="center" color="success">
                                    <MDTypography textAlign="center" fontWeight="bold" color="white">Feed Added Successfully!</MDTypography>
                                </MDAlert>
                                )}
                                </MDTypography>
                            </MDBox>
                        
                    </Card>
                </MDBox>
            </Grid>
        </DashboardLayout>
    );
}

export default AddFeed;