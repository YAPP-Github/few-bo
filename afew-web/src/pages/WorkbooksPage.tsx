import React, { useState, useEffect } from 'react';
import WorkbookList from '../components/workbook/WorkbookList';
import { getWorkbooks } from '../services/WorkbookService';
import { Workbook } from '../types/Workbook';

const WorkbooksPage: React.FC = () => {
  const [workbooks, setWorkbooks] = useState<Workbook[]>([]);

  useEffect(() => {
    const fetchWorkbooks = async () => {
      const workbooks = await getWorkbooks();
      setWorkbooks(workbooks);
    };
    fetchWorkbooks();
  }, []);

  return (
    <div>
      <h1>학습지 관리</h1>
      <WorkbookList workbooks={workbooks} />
    </div>
  );
};

export default WorkbooksPage;