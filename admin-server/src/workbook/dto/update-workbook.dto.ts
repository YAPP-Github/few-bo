import { PartialType } from '@nestjs/swagger';
import { CreateWorkbookDto } from './create-workbook.dto';

export class UpdateWorkbookDto extends PartialType(CreateWorkbookDto) {}
