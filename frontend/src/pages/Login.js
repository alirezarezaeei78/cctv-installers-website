import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage('');
    try {
      await axios.post('/api/login/', {
        username,
        password,
      });
      setMessage('ورود با موفقیت انجام شد.');
      setUsername('');
      setPassword('');
      setTimeout(() => navigate('/'), 2000);
    } catch (error) {
      console.error('Login error', error);
      setMessage('خطا در ورود. لطفاً نام کاربری و گذرواژه را بررسی کنید.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="row justify-content-center rtl-text">
      <div className="col-md-6">
        <h2 className="mb-4">ورود</h2>
        {message && <div className="alert alert-info">{message}</div>}
        <form onSubmit={handleSubmit} className="animate__animated animate__fadeIn">
          {/* Username input with icon */}
          <div className="mb-3">
            <label htmlFor="username" className="form-label">نام کاربری</label>
            <div className="input-group">
              <span className="input-group-text"><i className="fa fa-user"></i></span>
              <input
                type="text"
                className="form-control"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
          </div>
          {/* Password input with icon */}
          <div className="mb-3">
            <label htmlFor="password" className="form-label">گذرواژه</label>
            <div className="input-group">
              <span className="input-group-text"><i className="fa fa-lock"></i></span>
              <input
                type="password"
                className="form-control"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>
          {/* Submit button */}
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? 'در حال ارسال...' : 'ورود'}
          </button>
          <div className="mt-3">
            <small>
              حساب کاربری ندارید؟{' '}
              <a href="/register" className="text-decoration-none">ثبت‌نام کنید</a>
            </small>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;