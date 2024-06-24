import { Article } from '../types/Article';

const articles: Article[] = [
  { id: '1', title: '아티클 1', description: '아티클 1 소개' },
  { id: '2', title: '아티클 2', description: '아티클 2 소개' },
  { id: '3', title: '아티클 3', description: '아티클 3 소개' },
  { id: '4', title: '아티클 4', description: '아티클 4 소개' }
];

export const searchArticles = async (query: string): Promise<Article[]> => {
  return articles.filter(article => article.title.includes(query) || article.description.includes(query));
};