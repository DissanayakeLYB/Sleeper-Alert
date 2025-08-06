import home from "../../assets/NavBar/home.png";
import about from "../../assets/NavBar/about.png";
import contact from "../../assets/NavBar/phone.png";

function NavBar() {
    return (
        <nav className="flex items-center justify-around border-2 border-gray-300 py-6">
            <ul className="flex space-x-16 ">
                <a href="#home" className="flex items-center">
                    <img
                        src={home}
                        alt="Home"
                        className="h-5 w-5 inline-block mr-2"
                    />
                    <li>Home</li>
                </a>
                <a href="#about" className="flex items-center">
                    <img
                        src={about}
                        alt="About"
                        className="h-5 w-5 inline-block mr-2"
                    />
                    <li>About</li>
                </a>
                <a href="#contact" className="flex items-center">
                    <img
                        src={contact}
                        alt="Contact"
                        className="h-5 w-5 inline-block mr-2"
                    />
                    <li>Contact</li>
                </a>
            </ul>
        </nav>
    );
}

export default NavBar;
