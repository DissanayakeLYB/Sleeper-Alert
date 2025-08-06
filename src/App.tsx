import Footer from "./components/Home/Footer";
import Header from "./components/Home/Header";
import NavBar from "./components/Home/NavBar";

function App() {
    return (
        <div
            className=""
            style={{
                minHeight: "100vh",
                display: "flex",
                flexDirection: "column",
            }}
        >
            <Header />
            <NavBar />
            <main style={{ flex: 1 }}></main>
            <Footer />
        </div>
    );
}

export default App;
