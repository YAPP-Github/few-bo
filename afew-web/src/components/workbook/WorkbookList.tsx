import React from 'react';
import { List } from 'antd';
import { useNavigate } from 'react-router-dom';
import { Workbook } from '../../types/Workbook';

interface WorkbookListProps {
  workbooks: Workbook[];
}

const WorkbookList: React.FC<WorkbookListProps> = ({ workbooks }) => {
  const navigate = useNavigate();

  const goToDetail = (id: number) => {
    navigate(`/workbooks/${id}`);
  };

  return (
    <List
      itemLayout="horizontal"
      dataSource={workbooks}
      renderItem={(item) => (
        <List.Item>
          <List.Item.Meta
            title={<a onClick={() => goToDetail(item.id)}>{item.title}</a>}
            description={item.description}
          />
        </List.Item>
      )}
    />
  );
};

export default WorkbookList;