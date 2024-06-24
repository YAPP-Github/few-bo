import React from 'react';
import { Tabs } from 'antd';
import WritersPage from './WritersPage';
import WorkbooksPage from './WorkbooksPage';

const { TabPane } = Tabs;

const AdminPage: React.FC = () => (
  <Tabs defaultActiveKey="1">
    <TabPane tab="작가 관리" key="1">
      <WritersPage />
    </TabPane>
    <TabPane tab="학습지 관리" key="2">
      <WorkbooksPage />
    </TabPane>
  </Tabs>
);

export default AdminPage;