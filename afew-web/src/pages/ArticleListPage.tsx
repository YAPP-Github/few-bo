import React from 'react';
import { List, Card } from 'antd';
import { Link } from 'react-router-dom';
import articles from './diggin_result.json'; // JSON 파일을 import

const ArticleListPage: React.FC = () => {
  return (
    <div>
      <h2>아티클 리스트</h2>
      <List
        grid={{ gutter: 8, column: 1 }}
        dataSource={articles}
        renderItem={(item, index) => (
          <List.Item>
            <Link to={`/article/${index}`} state={item}>
              <Card hoverable>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <img
                    src={item.thumbnailImageURL}
                    alt={item.content.title}
                    style={{ width: 80, height: 80, objectFit: 'cover', marginRight: 20 }}
                  />
                  <div>
                    <h3 style={{ margin: 0 }}>{item.content.title}</h3>
                    <p style={{ margin: 0, color: '#888' }}>{item.content.category}</p>
                  </div>
                </div>
              </Card>
            </Link>
          </List.Item>
        )}
      />
    </div>
  );
};

export default ArticleListPage;