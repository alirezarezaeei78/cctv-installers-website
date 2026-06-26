import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="rtl-text">
      {/* Hero Section */}
      <div className="hero-section text-center animate__animated animate__fadeIn">
        <h1 className="display-5 fw-bold mb-3">بازار نصب دوربین مداربسته</h1>
        <p className="lead mb-4">
          خدمات حرفه‌ای نصب دوربین برای خانه، محل کار و ساختمان‌های اداری
        </p>
        <Link to="/request" className="btn btn-light btn-lg px-4 shadow">
          ثبت درخواست نصب
        </Link>
      </div>

      {/* How It Works Section */}
      <section className="mb-5">
        <h2 className="h4 text-center mb-4">چگونه کار می‌کند</h2>
        <div className="row g-4">
          <div className="col-md-4 text-center animate__animated animate__fadeInUp animate__delay-1s">
            <img
              src="https://img.icons8.com/ios-filled/100/4e73df/security-camera.png"
              alt="Submit request"
              className="mb-3"
            />
            <h5 className="mb-2">ثبت درخواست</h5>
            <p className="small">
              فرم چندمرحله‌ای درخواست را پر کنید و مشخصات کامل پروژه خود را ثبت
              کنید.
            </p>
          </div>
          <div className="col-md-4 text-center animate__animated animate__fadeInUp animate__delay-2s">
            <img
              src="https://img.icons8.com/ios-filled/100/4e73df/comparison.png"
              alt="Compare quotes"
              className="mb-3"
            />
            <h5 className="mb-2">مقایسه پیشنهادها</h5>
            <p className="small">
              پس از ارسال درخواست، نصاب‌های تایید شده پیشنهاد قیمت و زمانبندی
              خود را ارسال می‌کنند. شما می‌توانید آنها را مقایسه کنید.
            </p>
          </div>
          <div className="col-md-4 text-center animate__animated animate__fadeInUp animate__delay-3s">
            <img
              src="https://img.icons8.com/ios-filled/100/4e73df/ok--v1.png"
              alt="Choose installer"
              className="mb-3"
            />
            <h5 className="mb-2">انتخاب بهترین نصاب</h5>
            <p className="small">
              بر اساس قیمت، سابقه و امتیاز سایر مشتریان، بهترین نصاب را برای
              پروژه خود انتخاب نمایید.
            </p>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="text-center">
        <h3 className="mb-3">آماده‌اید امنیت محیط خود را افزایش دهید؟</h3>
        <Link to="/request" className="btn btn-primary btn-lg px-4">
          همین حالا شروع کنید
        </Link>
      </section>
    </div>
  );
}

export default Home;