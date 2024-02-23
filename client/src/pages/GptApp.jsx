import MDBox from "components/MDBox"
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
const Home = () => {
    return (
        <DashboardLayout>
            <DashboardNavbar />
        <MDBox py={3}>
        <div>        <iframe
            src="https://langchain-document-chat.streamlit.app/?embed=true"
            height="600"
            style={{ width: "100%", border: "none" }}
            ></iframe></div>
            </MDBox>
        </DashboardLayout>
    )
}

export default Home