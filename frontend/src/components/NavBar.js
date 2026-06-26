import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function NavBar() {
  const [expanded, setExpanded] = useState(false);
  const toggleMenu = () => setExpanded(!expanded);

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark rtl-text">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          نصب دوربین
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          onClick={toggleMenu}
          aria-controls="navbarSupportedContent"
          aria-expanded={expanded ? 'true' : 'false'}
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className={`collapse navbar-collapse${expanded ? ' show' : ''}`} id="navbarSupportedContent">
          {/* Use me-auto to push items to the right in RTL */}
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                صفحه اصلی
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/installers">
                نصاب‌ها
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/request">
                درخواست نصب
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/login">
                ورود
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/register">
                ثبت‌نام
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;