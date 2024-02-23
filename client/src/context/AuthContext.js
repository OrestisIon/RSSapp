import  { createContext, useContext, useState, useEffect } from 'react';
import PropTypes from 'prop-types'; 

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
        // Implement login logic here and update the user state
        //Extract the username and password from userData
        const { username, password } = userData;
        console.log('Logging in' + username + ' ' + password);
        const err = (s) => console.error(s)
        if (!(username && password)) {
            return new Promise((x, y) => {
                return null
            })
        }
        // Base64 encode the username and password
        const base64Credentials = btoa(username + ':' + password);
        const params = {
            headers: {
                'Authorization': 'Basic ' + base64Credentials,
                'Content-Type': 'application/json' // Assuming JSON is expected
            }
        };
        const server = import.meta.env.VITE_REACT_APP_MINIFLUX_API_URL
        const url = server + '/v1/me' // This is the URL for the Miniflux API
        return fetch(url, params)
            .then((r) => {
                if (!r.ok) {
                    throw r
                }
                if (r.status === 204) {
                    return r
                }
                localStorage.setItem('user', JSON.stringify(userData));
                setUser(userData);
                return r.json()
            })

            .catch((e) => {
                if (e instanceof TypeError) {
                    err(e.message)
                } else if (e instanceof Response) {
                    const contentType = e.headers.get('content-type')
                    if (
                        contentType &&
                        contentType.indexOf('application/json') !== -1
                    ) {
                        e.json().then((msg) => err(msg['error_message']))
                    } else {
                        e.text().then((msg) => err(msg))
                    }
                } else {
                    err(String(e))
                }
                return Promise.reject()
            })
        // Implement login logic here and update the user state
    };

    const logout = () => {
        // Clear user from local storage on logout
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
