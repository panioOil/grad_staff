import axios from 'axios';

// ให้มันจำ IP อัตโนมัติจาก URL ที่มือถือกำลังเปิดอยู่
const getBaseUrl = () => {
  const currentHost = window.location.hostname;
  return `http://${currentHost}:8001/api`; // หรือตามพอร์ต Backend ที่คุณตั้งไว้
};

const api = axios.create({
  baseURL: getBaseUrl(),
});

export default api;