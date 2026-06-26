import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Installers() {
  const [installers, setInstallers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchInstallers() {
      try {
        const response = await axios.get('/api/installers/');
        setInstallers(response.data);
      } catch (error) {
        console.error('Error fetching installers', error);
      } finally {
        setLoading(false);
      }
    }
    fetchInstallers();
  }, []);

  if (loading) {
    return <p>در حال بارگذاری ...</p>;
  }

  const verificationLabels = [
    'بدون تایید',
    'تایید هویت',
    'تایید مهارت',
    'تایید تجاری',
  ];

  return (
    <div className="rtl-text">
      <h2 className="mb-4">لیست نصاب‌ها</h2>
      {installers.length === 0 ? (
        <p>هیچ نصابی یافت نشد.</p>
      ) : (
        <div className="row g-4">
          {installers.map((installer) => {
            const level = installer.verification_level || 0;
            const badgeLabel = verificationLabels[level] || verificationLabels[0];
            return (
              <div className="col-md-6" key={installer.id}>
                <div className="card h-100 shadow-sm animate__animated animate__fadeInUp">
                  <div className="card-body">
                    <div className="d-flex align-items-center mb-2">
                      <h5 className="card-title mb-0 me-2">
                        {installer.user.username}
                        {installer.business_name && <span className="text-muted"> ({installer.business_name})</span>}
                      </h5>
                      {/* Example star rating: map verification level to number of stars */}
                      <div className="ms-auto">
                        {[...Array(5)].map((_, idx) => (
                          <span
                            key={idx}
                            className={`fa-solid fa-star${idx < level + 2 ? ' text-warning' : ' text-muted'}`}
                          ></span>
                        ))}
                      </div>
                    </div>
                    <p className="card-text mb-1">
                      <strong>شماره تماس:</strong> {installer.phone || '---'}
                    </p>
                    <p className="card-text mb-1">
                      <strong>آدرس:</strong> {installer.address || '---'}
                    </p>
                    {installer.bio && (
                      <p className="card-text mb-1">
                        <strong>توضیحات:</strong> {installer.bio}
                      </p>
                    )}
                  </div>
                  <div className="card-footer bg-transparent border-0 d-flex justify-content-between align-items-center">
                    <span className={`verification-badge level${level}`}>{badgeLabel}</span>
                    <button className="btn btn-outline-primary btn-sm">مشاهده پروفایل</button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Installers;