import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
  // Form fields
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('customer');
  const [businessName, setBusinessName] = useState('');
  const [address, setAddress] = useState('');
  const [bio, setBio] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage('');
    // Validate password confirmation
    if (password !== confirmPassword) {
      setMessage('گذرواژه و تکرار آن مطابقت ندارند.');
      setSubmitting(false);
      return;
    }
    try {
      await axios.post('/api/register/', {
        username,
        email,
        password,
        role,
        phone,
        business_name: businessName,
        address,
        bio,
      });
      setMessage('ثبت‌نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.');
      // Reset form fields
      setUsername('');
      setEmail('');
      setPhone('');
      setPassword('');
      setConfirmPassword('');
      setRole('customer');
      setBusinessName('');
      setAddress('');
      setBio('');
      setTimeout(() => navigate('/login'), 2000);
    } catch (error) {
      console.error('Registration error', error);
      setMessage('خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="row justify-content-center">
      <div className="col-md-6">
        <h2 className="mb-4">ثبت‌نام</h2>
        {message && <div className="alert alert-info">{message}</div>}
        <form onSubmit={handleSubmit} className="rtl-text">
          {/* Username */}
          <div className="mb-3">
            <label htmlFor="username" className="form-label">نام کاربری</label>
            <input
              type="text"
              className="form-control"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          {/* Email */}
          <div className="mb-3">
            <label htmlFor="email" className="form-label">ایمیل</label>
            <input
              type="email"
              className="form-control"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          {/* Phone */}
          <div className="mb-3">
            <label htmlFor="phone" className="form-label">شماره تماس</label>
            <input
              type="tel"
              className="form-control"
              id="phone"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
          </div>
          {/* Role selector */}
          <div className="mb-3">
            <label htmlFor="role" className="form-label">نوع کاربر</label>
            <select
              id="role"
              className="form-select"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="customer">مشتری</option>
              <option value="installer">نصاب</option>
            </select>
          </div>
          {/* Business name: only for installers */}
          {role === 'installer' && (
            <div className="mb-3">
              <label htmlFor="businessName" className="form-label">نام کسب و کار</label>
              <input
                type="text"
                className="form-control"
                id="businessName"
                value={businessName}
                onChange={(e) => setBusinessName(e.target.value)}
              />
            </div>
          )}
          {/* Address */}
          {role === 'installer' && (
            <div className="mb-3">
              <label htmlFor="address" className="form-label">آدرس</label>
              <input
                type="text"
                className="form-control"
                id="address"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
              />
            </div>
          )}
          {/* Bio */}
          {role === 'installer' && (
            <div className="mb-3">
              <label htmlFor="bio" className="form-label">توضیحات</label>
              <textarea
                className="form-control"
                id="bio"
                rows="3"
                value={bio}
                onChange={(e) => setBio(e.target.value)}
              ></textarea>
            </div>
          )}
          {/* Password */}
          <div className="mb-3">
            <label htmlFor="password" className="form-label">گذرواژه</label>
            <input
              type="password"
              className="form-control"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {/* Confirm password */}
          <div className="mb-3">
            <label htmlFor="confirmPassword" className="form-label">تکرار گذرواژه</label>
            <input
              type="password"
              className="form-control"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          {/* Submit button */}
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? 'در حال ارسال...' : 'ثبت‌نام'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Register;