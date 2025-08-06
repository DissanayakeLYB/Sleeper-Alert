import phone from "../../assets/Footer/phone.png";
import mail from "../../assets/Footer/mail.png";
import location from "../../assets/Footer/location.png";

function Footer() {
    return (
        <footer className="flex justify-around bg-gray-200 h-20 items-center">
            <div className="flex items-center">
                <img
                    className="mr-2"
                    width="20"
                    height="15"
                    src={mail}
                    alt="mail"
                />
                <p className="text-gray-500">
                    lasithdissanayake.official@gmail.com
                </p>
            </div>
            <div className="flex items-center">
                <img
                    className="mr-2"
                    width="20"
                    height="15"
                    src={phone}
                    alt="phone"
                />
                <p className="text-gray-500">+94 770212604</p>
            </div>
            <div className="flex items-center">
                <img
                    className="mr-2"
                    width="20"
                    height="15"
                    src={location}
                    alt="location"
                />
                <p className="text-gray-500">419/1, Mankada Road, Kadawatha</p>
            </div>
        </footer>
    );
}

export default Footer;
