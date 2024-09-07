// import React from 'react';
// import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
// import AdminPage from './pages/ArticleListPage';
// import WriterDetailPage from './pages/WriterDetailPage';
// import WorkbookDetailPage from './pages/WorkbookDetailPage';
// import './App.css'; 

// const App: React.FC = () => (
//   <Router>
//     <Routes>
//       <Route path="/" element={<AdminPage />} />
//       <Route path="/writers/:id" element={<WriterDetailPage />} />
//       <Route path="/workbooks/:id" element={<WorkbookDetailPage />} />
//     </Routes>
//   </Router>
// );

// export default App;

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ArticleListPage from './pages/ArticleListPage';
import ArticleDetailPage from './pages/ArticleDetailPage';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ArticleListPage/>} />
        <Route path="/article/:id" element={<ArticleDetailPage/>} />
      </Routes>
    </Router>
  );
};

export default App;