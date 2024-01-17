import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { createTask, deleteTask, updateTask, getTask } from '../api/tasks.api';
import { useNavigate, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';

export function TaskFormPage() {

    const { register, handleSubmit, formState: { errors }, setValue } = useForm();

    const navigate = useNavigate();

    const params = useParams();

    const onSubmit = handleSubmit(async data => {
        if (params.id) {
            await updateTask(params.id, data);
            toast.success('Task updated!', {position: 'top-right', style: {backgroundColor: 'green', color: 'white'}});
        } else { 
            await createTask(data);
            toast.success('Task created!', {position: 'top-right', style: {backgroundColor: 'green', color: 'white'}});
            navigate('/tasks');
        }
    })

    useEffect(() => {
        async function loadTask() {
            if (params.id) {
                const {data: {title, description}} = await getTask(params.id);
                setValue('title', title);
                setValue('description', description);
            }
        }
        loadTask();
    }, [params.id, setValue])

    return (
        <div className='max-w-xl mx-auto'>
            <form onSubmit={onSubmit}>
                <input type="text" placeholder="Title"
                    {...register("title", { required: true })}
                    className='bg-zinc-700 p-3 rounded-lg block w-full mb-3'
                />
                {errors.title && <span>This field is required</span>}

                <textarea rows="3" placeholder="Description"
                    {...register("description", { required: true })}
                    className='bg-zinc-700 p-3 rounded-lg block w-full mb-3'
                />
                {errors.description && <span>This field is required</span>}

                <button className='bg-indigo-500 p-3 rounded-lg block w-full mt-3'>Save</button>
            </form>

            {params.id && (
                <div className='flex justify-end'>
                    <button 
                        className='bg-red-500 p-3 rounded-lg w-48 mt-3'
                        onClick={async () => {
                        const confirmed = window.confirm('Are you sure?');
                        if (confirmed) {
                            await deleteTask(params.id);
                            toast.success('Task deleted!', {position: 'top-right', style: {backgroundColor: 'green', color: 'white'}});
                            navigate('/tasks');
                        }
                    }}>Delete</button>
                </div>
            )}
        </div>
    )
}