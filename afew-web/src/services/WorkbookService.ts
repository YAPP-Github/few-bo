import { Workbook } from '../types/Workbook';

let workbooks: Workbook[] = [
  { id: 1, thumbnail: '', title: '학습지 1', description: '학습지 1 소개', referencedArticles: ['아티클 1', '아티클 3'] },
  { id: 2, thumbnail: '', title: '학습지 2', description: '학습지 2 소개', referencedArticles: ['아티클 2', '아티클 4'] }
];

export const getWorkbooks = async (): Promise<Workbook[]> => {
  return workbooks;
};

export const getWorkbook = async (id: number): Promise<Workbook | undefined> => {
  return workbooks.find(workbook => workbook.id === id);
};

export const updateWorkbook = async (id: number, data: Partial<Workbook>): Promise<void> => {
  workbooks = workbooks.map(workbook => (workbook.id === id ? { ...workbook, ...data } : workbook));
};