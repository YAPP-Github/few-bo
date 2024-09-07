import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Input, Button, List, Card, Collapse, Row, Col } from 'antd';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';

const { TextArea } = Input;
const { Panel } = Collapse;

interface Article {
  link: string;
  thumbnailImageURL: string;
  content: {
    title: string;
    body: string;
    category: string;
    description: string;
    questions: {
      title: string;
      contents: { number: number; content: string }[];
      answer: number;
      explanation: string;
    }[];
  };
}

interface LocationState {
  article: Article;
}

const ArticleDetailPage: React.FC = () => {
  const location = useLocation();
  const state = location.state as Article | undefined;
  const [data, setData] = useState<Article | null>(state || null);
  const [selectedBody, setSelectedBody] = useState<string>(data?.content.body || '');

  useEffect(() => {
    if (state) {
      setData(state);
      setSelectedBody(state.content.body);
    }
  }, [state]);

  if (!data) {
    console.log(state);
    return <div>아티클 데이터를 불러올 수 없습니다.</div>;
  }

  // 개별 질문 데이터 편집
  const handleQuestionChange = (index: number, field: string, value: any) => {
    const updatedQuestions = [...data.content.questions];
    updatedQuestions[index] = { ...updatedQuestions[index], [field]: value };
    setData({
      ...data,
      content: { ...data.content, questions: updatedQuestions },
    });
  };

  // Link, Thumbnail URL, Title, Body, Category, Description 데이터 편집
  const handleContentChange = (field: string, value: any) => {
    setData({
      ...data,
      content: { ...data.content, [field]: value },
    });
  };

  // 커스텀 렌더러로 이미지 크기를 조정
  const renderers = {
    img: (props: JSX.IntrinsicElements['img']) => (
      <img
        {...props}
        style={{ maxWidth: '100%', height: 'auto', display: 'block', margin: '0 auto' }}
      />
    ),
  };

  return (
    <div>
      <h2>콘텐츠 관리</h2>
      <Card title="콘텐츠 정보">
        <Input
          addonBefore="Link"
          value={data.link}
          onChange={(e) => setData({ ...data, link: e.target.value })}
        />
        <Input
          addonBefore="Thumbnail Image URL"
          value={data.thumbnailImageURL}
          onChange={(e) => setData({ ...data, thumbnailImageURL: e.target.value })}
        />
        <Input
          addonBefore="Title"
          value={data.content.title}
          onChange={(e) => handleContentChange('title', e.target.value)}
        />
        <Input
          addonBefore="Body"
          value={data.content.body}
          onChange={(e) => handleContentChange('body', e.target.value)}
        />
        <Input
          addonBefore="Category"
          value={data.content.category}
          onChange={(e) => handleContentChange('category', e.target.value)}
        />
        <Input
          addonBefore="Description"
          value={data.content.description}
          onChange={(e) => handleContentChange('description', e.target.value)}
        />
      </Card>

      <h2>질문 관리</h2>
      <Collapse accordion>
        {data.content.questions?.map((question, index) => (
          <Panel header={question.title} key={index}>
            <Card title={`질문 ${index + 1}`}>
              <Input
                addonBefore="Title"
                value={question.title}
                onChange={(e) => handleQuestionChange(index, 'title', e.target.value)}
              />
              <Input
                addonBefore="Explanation"
                value={question.explanation}
                onChange={(e) => handleQuestionChange(index, 'explanation', e.target.value)}
              />
              <List
                header={<div>Options</div>}
                bordered
                dataSource={question.contents}
                renderItem={(item) => (
                  <List.Item>
                    <Input
                      value={item.content}
                      onChange={(e) => {
                        const updatedContents = question.contents.map((opt) =>
                          opt.number === item.number
                            ? { ...opt, content: e.target.value }
                            : opt
                        );
                        handleQuestionChange(index, 'contents', updatedContents);
                      }}
                    />
                  </List.Item>
                )}
              />
              <Input
                addonBefore="Answer"
                value={question.answer}
                onChange={(e) => handleQuestionChange(index, 'answer', e.target.value)}
              />
            </Card>
          </Panel>
        ))}
      </Collapse>

      <h2>아티클 관리</h2>
      <Row gutter={16}>
        <Col span={12}>
          <Card title="원본 Body 리스트">
            <List
              dataSource={[data.content.body]}
              renderItem={(body, index) => (
                <List.Item key={index} onClick={() => setSelectedBody(body)}>
                  <div>{body}</div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Markdown 뷰어">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
              components={renderers}
            >
              {selectedBody}
            </ReactMarkdown>
          </Card>
        </Col>
      </Row>

      <Button type="primary" onClick={() => console.log(data)}>
        Save
      </Button>
    </div>
  );
};

export default ArticleDetailPage;