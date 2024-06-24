import { Writer } from '../types/Writer';

let writers: Writer[] = [
  { id: 1, name: '작가 1', description: '작가 1 소개', articles: ['아티클 1', '아티클 2'] },
  { id: 2, name: '작가 2', description: '작가 2 소개', articles: ['아티클 3', '아티클 4'] }
];

export const getWriters = async (): Promise<Writer[]> => {
  return writers;
};

export const getWriter = async (id: number): Promise<Writer | undefined> => {
  return writers.find(writer => writer.id === id);
};

export const updateWriter = async (id: number, data: Partial<Writer>): Promise<void> => {
  writers = writers.map(writer => (writer.id === id ? { ...writer, ...data } : writer));
};