import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Form, Input, Button, List } from 'antd';
import { getWorkbook, updateWorkbook } from '../services/WorkbookService';
import { Workbook } from '../types/Workbook';
import ArticleSearch from '../components/ArticleSearch';

const WorkbookDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [workbook, setWorkbook] = useState<Workbook | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    const fetchWorkbook = async () => {
      const workbookData = await getWorkbook(Number(id));
      if (workbookData) {
        setWorkbook(workbookData);
        form.setFieldsValue(workbookData);
      } else {
        // Handle the case when the workbook is not found
        console.error('Workbook not found');
      }
    };
    fetchWorkbook();
  }, [id, form]);

  const onFinish = async (values: any) => {
    if (workbook) {
      const updatedWorkbook = { ...workbook, ...values };
      await updateWorkbook(workbook.id, updatedWorkbook);
      setWorkbook(updatedWorkbook);
    }
  };

  const addArticleToWorkbook = (articleId: string) => {
    if (workbook) {
      const updatedArticles = [...workbook.referencedArticles, articleId];
      const updatedWorkbook = { ...workbook, referencedArticles: updatedArticles };
      setWorkbook(updatedWorkbook);
      form.setFieldsValue(updatedWorkbook);
    }
  };

  return workbook ? (
    <div>
      <h1>{workbook.title} 상세 페이지</h1>
      <Form form={form} layout="vertical" onFinish={onFinish}>
        <Form.Item name="thumbnail" label="썸네일 URL" rules={[{ required: true, message: '썸네일 URL을 입력해주세요' }]}>
          <Input />
        </Form.Item>
        <Form.Item name="title" label="학습지 제목" rules={[{ required: true, message: '제목을 입력해주세요' }]}>
          <Input />
        </Form.Item>
        <Form.Item name="description" label="학습지 소개" rules={[{ required: true, message: '소개를 입력해주세요' }]}>
          <Input.TextArea rows={4} />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">저장</Button>
        </Form.Item>
      </Form>
      <h2>아티클 리스트</h2>
      <ArticleSearch onAdd={addArticleToWorkbook} />
      <List
        itemLayout="horizontal"
        dataSource={workbook.referencedArticles}
        renderItem={(articleId) => (
          <List.Item>
            <List.Item.Meta
              title={`아티클 ${articleId}`}
            />
          </List.Item>
        )}
      />
    </div>
  ) : (
    <div>Loading...</div>
  );
};

export default WorkbookDetailPage;