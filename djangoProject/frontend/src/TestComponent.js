import React, {useState} from 'react';
import axiosInstance from './api/axiosConfig';

const TestComponent = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: '',
    });

    const [errors, setErrors] = useState({});


    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Client-side check for password match
        if (formData.password !== formData.confirmPassword) {
            setErrors({confirmPassword: "Passwords do not match."});
            return;
        }

        try {
            const response = await axiosInstance.post('auth/signup/', {
                email: formData.email,
                password: formData.password,
                confirm_password: formData.confirmPassword,
            });
            console.log("User registered:", response.data);
            alert("Please check your email to verify your account.");
            setErrors({});
        } catch (error) {
            if (error.response && error.response.data) {
                setErrors(error.response.data);
            } else {
                console.error("An unexpected error occurred:", error);
            }
        }
    };


    return (
        <form onSubmit={handleSubmit}>
            {errors.non_field_errors && <p className="error">{errors.non_field_errors}</p>}

            <label>
                Email:
                {errors.email && <p className="error">{errors.email}</p>}
                <input type="email" name="email" value={formData.email} onChange={handleChange} required/>
            </label>
            <br/>

            <label>
                Password:
                {errors.password && <p className="error">{errors.password}</p>}
                <input type="password" name="password" value={formData.password} onChange={handleChange} required/>
            </label>
            <br/>

            <label>
                Confirm Password:
                {errors.confirmPassword && <p className="error">{errors.confirmPassword}</p>}
                <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange}
                       required/>
            </label>
            <br/>

            <button type="submit">Sign Up</button>
        </form>
    );
};

export default TestComponent;
