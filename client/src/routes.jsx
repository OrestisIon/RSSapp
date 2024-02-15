
import Dashboard from "pages/dashboard";
import Login from "pages/auth/Login";
import Signup from "pages/auth/Signup";
import CategoriesFeeds from "pages/CategoriesFeeds";
import FeedBrowser from "pages/FeedBrowser";
import EditFeeds from "pages/EditFeeds";

// @mui icons
import Icon from "@mui/material/Icon";

const routes = [
    {
        type: "collapse",
        name: "Dashboard",
        key: "dashboard",
        icon: <Icon fontSize="small">dashboard</Icon>,
        route: "/dashboard",
        component: Dashboard,
    },
    // {
    //     type: "collapse",
    //     name: "RTL",
    //     key: "rtl",
    //     icon: <Icon fontSize="small">format_textdirection_r_to_l</Icon>,
    //     route: "/rtl",
    //     component: RTL,
    // },
    // {
    //     type: "collapse",
    //     name: "Notifications",
    //     key: "notifications",
    //     icon: <Icon fontSize="small">notifications</Icon>,
    //     route: "/notifications",
    //     component: Notifications,
    // },
    {
        type: "collapse",
        name: "Sign In",
        key: "sign-in",
        icon: <Icon fontSize="small">login</Icon>,
        route: "/login",
        component: Login,
    },
    {
        type: "collapse",
        name: "Sign Up",
        key: "sign-up",
        icon: <Icon fontSize="small">assignment</Icon>,
        route: "/register",
        component: Signup,
    },
    {
        type: "collapse",
        name: "Categories",
        key: "categories",
        icon: <Icon fontSize="small">assignment</Icon>,
        route: "/categories-feeds",
        component: CategoriesFeeds,
    },
    {
        type: "collapse",
        name: "All Feeds",
        key: "all-feeds",
        icon: <Icon fontSize="small">assignment</Icon>,
        route: "/all-feeds",
        component: FeedBrowser,
    },
    {
        type: "collapse",
        name: "Edit Feeds",
        key: "edit-feed",
        icon: <Icon fontSize="small">assignment</Icon>,
        route: "/edit-feeds",
        component: EditFeeds,
    },

];

export default routes;