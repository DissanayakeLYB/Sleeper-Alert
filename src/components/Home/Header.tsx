import user from "../../assets/Header/user.png";

function Header() {
    return (
        <header className="flex items-center justify-between py-10 px-20 ">
            <h1 className="text-2xl font-bold">My Website</h1>
            <img src={user} alt="user profile picture" className="h-14" />
        </header>
    );
}

export default Header;
