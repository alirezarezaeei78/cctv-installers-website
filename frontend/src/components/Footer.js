import React from 'react';

function Footer() {
  return (
    <footer className="bg-dark text-light py-4 mt-auto">
      <div className="container">
        <div className="row">
          <div className="col-md-4 mb-3">
            <h5 className="mb-2">درباره ما</h5>
            <p className="small">
              ما یک بازار تخصصی نصب دوربین مداربسته هستیم که به شما کمک می‌کند
              بهترین نصاب‌های تایید شده را برای خانه و محل کار خود پیدا کنید.
            </p>
          </div>
          <div className="col-md-4 mb-3">
            <h5 className="mb-2">لینک‌های مفید</h5>
            <ul className="list-unstyled">
              <li><a href="/" className="text-light">صفحه اصلی</a></li>
              <li><a href="/installers" className="text-light">نصاب‌ها</a></li>
              <li><a href="/pricing" className="text-light">راهنمای قیمت</a></li>
              <li><a href="/help" className="text-light">مرکز راهنما</a></li>
            </ul>
          </div>
          <div className="col-md-4 mb-3">
            <h5 className="mb-2">تماس با ما</h5>
            <p className="small mb-1">ایمیل: info@example.com</p>
            <p className="small mb-0">تلفن: ۰۲۱-۱۲۳۴۵۶۷۸</p>
          </div>
        </div>
        <div className="text-center mt-3">
          <small>© ۲۰۲۶ نصب دوربین مدار بسته. تمام حقوق محفوظ است.</small>
        </div>
      </div>
    </footer>
  );
}

export default Footer;