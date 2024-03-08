import  { createContext, useContext, useState, useEffect } from 'react';
import PropTypes from 'prop-types'; 
import axios from 'axios';
const AuthContext = createContext();

export function useAuth() {
    return useContext(AuthContext);
}

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    // Load user from localStorage on initial load
    useEffect(() => {
        const storedUserData = localStorage.getItem('user');
        if (storedUserData) {
            setUser(JSON.parse(storedUserData));
        }
    }, []);
    const login = async (userData) => {
        // Extract the username and password from userData
        const { username, password } = userData;
        console.log('Logging in', username, password);

        if (!username || !password) {
            // If username or password is missing, resolve to null immediately
            return Promise.resolve(null);
        }

        // Prepare the data for the request
        const data = {
            username: username,
            password: password,
        };

        // Define the URL for the login request
        const server = import.meta.env.VITE_REACT_APP_MINIFLUX_API_URL;
        const url = `${server}/token`; // Adjust this to your actual login URL
        try {
            axios({ method: 'post', url: url, data: data })
                .then((response) => {
                    console.log('Login successful', response.data);
                    localStorage.setItem('jwt-token', response.data.access_token);
                    return response.data;
                })
                .catch((error) => {
                    console.error('Login error:', error);
                    // Handle error as needed
                    return Promise.reject();
                });
        } catch (error) {
            console.error('Login error:', error);
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx and the error response might have data
                console.error('Error data:', error.response.data);
                const errorMessage = error.response.data.error_message || 'An error occurred';
                console.error(errorMessage);
                // You can adjust the error handling as needed
            } else if (error.request) {
                // The request was made but no response was received
                console.error('No response received from the server.');
            } else {
                // Something happened in setting up the request that triggered an Error
                console.error('Error', error.message);
            }
            return Promise.reject();
        }
    };


    // const login = async (userData) => {
    //     const { username, password } = userData;
    //     console.log('Logging in', username, password);

    //     if (!username || !password) {
    //         return Promise.resolve(null);
    //     }

    //     // Prepare the data for x-www-form-urlencoded format
    //     const data = qs.stringify({
    //         grant_type: '', // adjust as necessary, left empty as per the curl example
    //         username: username,
    //         password: password,
    //         scope: '', // adjust as necessary, left empty as per the curl example
    //         client_id: '', // adjust as necessary, left empty as per the curl example
    //         client_secret: '', // adjust as necessary, left empty as per the curl example
    //     });

    //     // Define the URL for the login request
    //     const server = import.meta.env.VITE_REACT_APP_MINIFLUX_API_URL;
    //     const url = `${server}/token`;

    //     try {
    //         const response = await axios({
    //             method: 'post',
    //             url: url,
    //             data: data,
    //             headers: {
    //                 'Content-Type': 'application/x-www-form-urlencoded',
    //             },
    //         });

    //         console.log('Login successful', response.data);
    //         localStorage.setItem('jwt-token', response.data.access_token);
    //         return response.data;
    //     } catch (error) {
    //         console.error('Login error:', error);
    //         // Handle error as needed
    //         return Promise.reject();
    //     }
    // };


    const logout = () => {
        // Clear user from local storage on logout
        localStorage.removeItem('jwt-token');
        localStorage.removeItem('user');
        // Implement logout logic here
        setUser(null);
    };

    const value = {
        user,
        login,
        logout,
    };

    AuthProvider.propTypes = {
        children: PropTypes.node.isRequired,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
