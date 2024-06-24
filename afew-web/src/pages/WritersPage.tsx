import React, { useState, useEffect } from 'react';
import WriterList from '../components/WriterList';
import { getWriters } from '../services/WriterService';
import { Writer } from '../types/Writer';

const WritersPage: React.FC = () => {
  const [writers, setWriters] = useState<Writer[]>([]);

  useEffect(() => {
    const fetchWriters = async () => {
      const writers = await getWriters();
      setWriters(writers);
    };
    fetchWriters();
  }, []);

  return (
    <div>
      <h1>작가 관리</h1>
      <WriterList writers={writers} />
    </div>
  );
};

export default WritersPage;