import { forwardRef } from "react";
import { twMerge } from "tailwind-merge";

interface InputProps
    extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = forwardRef<HTMLInputElement, InputProps>(({
    ...props
}, ref) => {
    return (
        <input className={twMerge(`flex w-[50%] bg-neutral-100 border border-transparent outline-none p-3 text-xl`)} ref={ref} {...props}/>
    )
})

Input.displayName = "Input";
 
export default Input;