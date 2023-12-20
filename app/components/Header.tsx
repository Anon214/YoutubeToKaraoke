import { CiYoutube } from "react-icons/ci";


const Header = () => {
    return ( 
        <div className="w-full flex justify-between p-4 h-[8vh] items-center bg-cyan-800 text-white">
            <div className='flex items-center '>
                <CiYoutube size={40} />
                <div className="font-bold text-lg pl-1">Youtube To Karaoke</div>
            </div>
            <a>github link</a>
        </div>
     );
}
 
export default Header;