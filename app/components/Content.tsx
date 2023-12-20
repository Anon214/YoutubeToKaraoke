"use client";

import Input from './Input'
import Button from './Button'
import { FieldValues, SubmitHandler, useForm} from 'react-hook-form'
import axios from 'axios'

const Content = () => {

    const {
        register,
        handleSubmit
    } = useForm<FieldValues>({
        defaultValues: {
            url: ''
        }
    })

    const onSubmit:SubmitHandler<FieldValues> = async (values) => {
        // console.log(values.link)
        try {
            // Send text to the backend
            const response = await axios.post('http://localhost:8000/process_link', { url: values.url }, { responseType: 'blob' });
        
            // Create a blob from the response data
            const blob = new Blob([response.data], { type: 'audio/wav' });
        
            // Create a link element and trigger a download
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'accompaniment.wav';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          } catch (error) {
            console.error('Error processing text:', error);
          }
    }

    return (
        //input of youtube link + output of download
            <form onSubmit={handleSubmit(onSubmit)}>
                <div className="flex flex-col pt-6 justify-center items-center">
                    <Input {...register('url')} placeholder="Enter Youtube URL Here..."/>
                    <div className="pt-6">
                        <Button type="submit">Convert</Button>
                    </div>
                </div>
            </form>
     );
}
 
export default Content;