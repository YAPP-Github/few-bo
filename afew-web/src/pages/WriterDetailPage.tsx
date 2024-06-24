import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Form, Input, Button } from 'antd';
import { getWriter, updateWriter } from '../services/WriterService';
import { Writer } from '../types/Writer';

const WriterDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [writer, setWriter] = useState<Writer | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    const fetchWriter = async () => {
      const writerData = await getWriter(Number(id));
      if (writerData) {
        setWriter(writerData);
        form.setFieldsValue(writerData);
      } else {
        // Handle the case when the writer is not found
        console.error('Writer not found');
      }
    };
    fetchWriter();
  }, [id, form]);

  const onFinish = async (values: any) => {
    if (writer) {
      await updateWriter(writer.id, values);
      setWriter({ ...writer, ...values });
    }
  };

  return writer ? (
    <div>
      <h1>{writer.name} 상세 페이지</h1>
      <Form form={form} layout="vertical" onFinish={onFinish}>
        <Form.Item name="name" label="작가 이름" rules={[{ required: true, message: '이름을 입력해주세요' }]}>
          <Input />
        </Form.Item>
        <Form.Item name="description" label="작가 소개" rules={[{ required: true, message: '소개를 입력해주세요' }]}>
          <Input.TextArea rows={4} />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">저장</Button>
        </Form.Item>
      </Form>
      <h2>아티클 리스트</h2>
      <ul>
        {writer.articles.map(article => (
          <li key={article}>{article}</li>
        ))}
      </ul>
    </div>
  ) : (
    <div>Loading...</div>
  );
};

export default WriterDetailPage;