import React, { useState } from 'react';
import { Input, List, Button } from 'antd';
import { searchArticles } from '../services/ArticleService';
import { Article } from '../types/Article';

interface ArticleSearchProps {
  onAdd: (articleId: string) => void;
}

const ArticleSearch: React.FC<ArticleSearchProps> = ({ onAdd }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Article[]>([]);

  const handleSearch = async () => {
    const articles = await searchArticles(query);
    setResults(articles);
  };

  return (
    <div>
      <Input.Search
        placeholder="Search articles"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onSearch={handleSearch}
      />
      <List
        itemLayout="horizontal"
        dataSource={results}
        renderItem={(item) => (
          <List.Item
            actions={[<Button onClick={() => onAdd(item.id)}>Add</Button>]}
          >
            <List.Item.Meta
              title={item.title}
              description={item.description}
            />
          </List.Item>
        )}
      />
    </div>
  );
};

export default ArticleSearch;