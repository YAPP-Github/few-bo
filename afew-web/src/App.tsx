import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import AdminPage from './pages/AdminPage';
import WriterDetailPage from './pages/WriterDetailPage';
import WorkbookDetailPage from './pages/WorkbookDetailPage';
import './App.css'; 

const App: React.FC = () => (
  <Router>
    <Routes>
      <Route path="/" element={<AdminPage />} />
      <Route path="/writers/:id" element={<WriterDetailPage />} />
      <Route path="/workbooks/:id" element={<WorkbookDetailPage />} />
    </Routes>
  </Router>
);

export default App;