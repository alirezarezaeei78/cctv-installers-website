import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

/**
 * Multi‑step request wizard for posting CCTV installation jobs.
 *
 * This component guides users through several steps to capture
 * structured demand data such as their buyer persona, property
 * characteristics, scheduling preferences, and job description.
 * A progress bar indicates how far along the user is. On the last
 * step, the collected data is submitted to the backend via a
 * multipart form request so file attachments can be uploaded.
 */
function RequestForm() {
  const navigate = useNavigate();
  // Wizard step index (1‑based for readability)
  const [step, setStep] = useState(1);
  // Form fields
  const [buyerType, setBuyerType] = useState('home');
  const [propertyType, setPropertyType] = useState('');
  const [address, setAddress] = useState('');
  const [preferredDate, setPreferredDate] = useState('');
  const [preferredTime, setPreferredTime] = useState('');
  const [urgency, setUrgency] = useState('medium');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [files, setFiles] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  // Progress percentage for the progress bar
  const progress = (step / 3) * 100;

  // Handlers for step navigation
  const handleNext = () => setStep((prev) => Math.min(prev + 1, 3));
  const handlePrev = () => setStep((prev) => Math.max(prev - 1, 1));

  // Handle file selection. Accept multiple files.
  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  // Submit the request to the backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage('');
    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('description', description);
      formData.append('buyer_type', buyerType);
      formData.append('property_type', propertyType);
      formData.append('address', address);
      formData.append('preferred_date', preferredDate);
      formData.append('preferred_time', preferredTime);
      formData.append('urgency', urgency);
      // Append files if any
      files.forEach((file) => formData.append('uploaded_files', file));
      await axios.post('/api/requests/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setMessage('درخواست شما با موفقیت ثبت شد.');
      // Reset fields
      setStep(1);
      setBuyerType('home');
      setPropertyType('');
      setAddress('');
      setPreferredDate('');
      setPreferredTime('');
      setUrgency('medium');
      setTitle('');
      setDescription('');
      setFiles([]);
      setTimeout(() => navigate('/'), 3000);
    } catch (error) {
      console.error('Error submitting request', error);
      setMessage('خطا در ثبت درخواست. لطفاً دوباره تلاش کنید.');
    } finally {
      setSubmitting(false);
    }
  };

  // Render the fields for each step
  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="form-step">
            <h5 className="mb-3">مرحله ۱: اطلاعات عمومی</h5>
            <div className="mb-3">
              <label className="form-label">شما چه کسی هستید؟</label>
              <select
                className="form-select"
                value={buyerType}
                onChange={(e) => setBuyerType(e.target.value)}
              >
                <option value="home">مالک خانه</option>
                <option value="business">مالک کسب‌وکار کوچک</option>
                <option value="manager">مدیر ساختمان</option>
              </select>
            </div>
            <div className="mb-3">
              <label className="form-label">نوع ملک</label>
              <input
                type="text"
                className="form-control"
                value={propertyType}
                onChange={(e) => setPropertyType(e.target.value)}
                placeholder="مثلاً: آپارتمان، ویلا، فروشگاه"
              />
            </div>
            <div className="mb-3">
              <label className="form-label">آدرس</label>
              <input
                type="text"
                className="form-control"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="آدرس دقیق محل نصب"
              />
            </div>
          </div>
        );
      case 2:
        return (
          <div className="form-step">
            <h5 className="mb-3">مرحله ۲: زمان و فوریت</h5>
            <div className="mb-3">
              <label className="form-label">تاریخ ترجیحی</label>
              <input
                type="date"
                className="form-control"
                value={preferredDate}
                onChange={(e) => setPreferredDate(e.target.value)}
              />
            </div>
            <div className="mb-3">
              <label className="form-label">زمان ترجیحی</label>
              <select
                className="form-select"
                value={preferredTime}
                onChange={(e) => setPreferredTime(e.target.value)}
              >
                <option value="">انتخاب کنید</option>
                <option value="morning">صبح (۸-۱۲)</option>
                <option value="afternoon">عصر (۱۲-۱۶)</option>
                <option value="evening">شب (۱۶-۲۰)</option>
              </select>
            </div>
            <div className="mb-3">
              <label className="form-label">سطح فوریت</label>
              <select
                className="form-select"
                value={urgency}
                onChange={(e) => setUrgency(e.target.value)}
              >
                <option value="low">کم</option>
                <option value="medium">متوسط</option>
                <option value="high">زیاد</option>
              </select>
            </div>
          </div>
        );
      case 3:
        return (
          <div className="form-step">
            <h5 className="mb-3">مرحله ۳: توضیحات و فایل‌ها</h5>
            <div className="mb-3">
              <label className="form-label">عنوان درخواست</label>
              <input
                type="text"
                className="form-control"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="عنوان مختصر برای درخواست"
                required
              />
            </div>
            <div className="mb-3">
              <label className="form-label">توضیحات</label>
              <textarea
                className="form-control"
                rows="4"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="توضیحات کامل شامل تعداد دوربین‌ها، برند دلخواه، و سایر نکات"
                required
              ></textarea>
            </div>
            <div className="mb-3">
              <label className="form-label">فایل‌های ضمیمه (اختیاری)</label>
              <input
                type="file"
                className="form-control"
                multiple
                onChange={handleFileChange}
              />
              {files && files.length > 0 && (
                <ul className="small mt-2">
                  {files.map((file, idx) => (
                    <li key={idx}>{file.name}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="row justify-content-center">
      <div className="col-md-8">
        <h2 className="mb-4 rtl-text">ثبت درخواست نصب دوربین</h2>
        {message && <div className="alert alert-info">{message}</div>}
        <div className="mb-3">
          <div className="progress" style={{ height: '8px' }}>
            <div
              className="progress-bar"
              role="progressbar"
              style={{ width: `${progress}%` }}
              aria-valuenow={progress}
              aria-valuemin="0"
              aria-valuemax="100"
            ></div>
          </div>
        </div>
        <form onSubmit={handleSubmit} className="animate__animated animate__fadeIn">
          {renderStep()}
          <div className="d-flex justify-content-between mt-4">
            {step > 1 && (
              <button type="button" className="btn btn-outline-secondary" onClick={handlePrev} disabled={submitting}>
                مرحله قبلی
              </button>
            )}
            {step < 3 && (
              <button type="button" className="btn btn-primary ms-auto" onClick={handleNext}>
                مرحله بعدی
              </button>
            )}
            {step === 3 && (
              <button type="submit" className="btn btn-success ms-auto" disabled={submitting}>
                {submitting ? 'در حال ارسال...' : 'ثبت درخواست'}
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}

export default RequestForm;