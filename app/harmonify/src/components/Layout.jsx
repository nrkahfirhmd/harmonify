import { Outlet } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";

const Layout = () => {
    return (
        <div className="px-5 md:px-20 bg-[#F8F4E1] w-full min-h-screen flex flex-col gap-5">
            <Header />
            <Outlet />
            <Footer />
        </div>
    )
}

export default Layout;