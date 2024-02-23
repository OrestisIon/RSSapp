
import Dashboard from "pages/dashboard";
import Login from "pages/auth/Login";
import Signup from "pages/auth/Signup";
import CategoriesFeeds from "pages/CategoriesFeeds";
import AllFeeds from "pages/AllFeeds";
import EditFeeds from "pages/EditFeeds";
import FeedIcon from '@mui/icons-material/Feed';
import EditIcon from '@mui/icons-material/Edit';
// @mui icons
import Icon from "@mui/material/Icon";
import AddIcon from '@mui/icons-material/Add';
import DashboardIcon from '@mui/icons-material/Dashboard';
import BookmarksIcon from '@mui/icons-material/Bookmarks';
import ForYou from "pages/ForYou";
import MySubscriptions from "pages/MySubscriptions";
import GptApp from "pages/GptApp";
const routes = [
    {
        type: "title",
        title: "Personailzed",
        name: "personailzed",
        key: "personailzed",
        icon: <Icon fontSize="small">assignment</Icon>,
    },
    {
        type: "collapse",
        name: "For You",
        key: "dashboard",
        icon: <DashboardIcon fontSize="small"></DashboardIcon>,
        route: "/dashboard",
        component: Dashboard,
    },
    {
        type: "collapse",
        name: "For You",
        key: "fyp",
        icon: <Icon fontSize="small">FY</Icon>,
        route: "/foryoupage",
        component: ForYou,
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
        name: "Saved",
        key: "saved",
        icon: <BookmarksIcon fontSize="small"></BookmarksIcon>,
        route: "/categories-feeds",
        component: CategoriesFeeds,
    },
    {
        type: "divider",
        key: "all-feeds-divider",
        icon: <Icon fontSize="small">assignment</Icon>,
    },
    {
        type: "title",
        title: "All Feeds",
        name: "All Feeds",
        key: "d1",
    },
    {
        type: "collapse",
        name: "All Feeds",
        key: "all-feeds",
        icon: <FeedIcon fontSize="small"></FeedIcon>,
        route: "/all-feeds",
        component: AllFeeds,
    },
    {
        type: "collapse",
        name: "Edit Feeds",
        key: "edit-feed",
        icon: <EditIcon fontSize="small"></EditIcon>,
        route: "/edit-feeds",
        component: EditFeeds,
    },
    {
        type: "collapse",
        name: "AI Chat",
        key: "gpt-app",
        icon: <EditIcon fontSize="small"></EditIcon>,
        route: "/gpt-app",
        component: GptApp,
    },
    {
        type: "collapse",
        name: "My Subscriptions",
        key: "my-subscriptions",
        icon: <Icon fontSize="small">subscriptions</Icon>,
        route: "/my-subscriptions",
        component: MySubscriptions,
    },
    {
        type: "collapse",
        name: "Add Category",
        key: "add-category",
        icon: <AddIcon fontSize="small">assignment</AddIcon>,
        route: "/edit-feeds",
        component: EditFeeds,
    },

];

export default routes;