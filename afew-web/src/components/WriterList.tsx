import React from 'react';
import { List } from 'antd';
import { useNavigate } from 'react-router-dom';
import { Writer } from '../types/Writer';

interface WriterListProps {
  writers: Writer[];
}

const WriterList: React.FC<WriterListProps> = ({ writers }) => {
  const navigate = useNavigate();

  const goToDetail = (id: number) => {
    navigate(`/writers/${id}`);
  };

  return (
    <List
      itemLayout="horizontal"
      dataSource={writers}
      renderItem={(item) => (
        <List.Item>
          <List.Item.Meta
            title={<a onClick={() => goToDetail(item.id)}>{item.name}</a>}
            description={item.description}
          />
        </List.Item>
      )}
    />
  );
};

export default WriterList;