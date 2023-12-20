import { forwardRef } from "react";
import { twMerge } from "tailwind-merge";

interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(({
    children,
    type = "button",
    ...props
}, ref) => {
    return (
        <button type={type} className={twMerge(`bg-blue-500 rounded-md h-[54px] w-[140px] hover:opacity-75 transition text-white`)}>
            {children}
        </button>
    )
})

Button.displayName = "Button";
 
export default Button;