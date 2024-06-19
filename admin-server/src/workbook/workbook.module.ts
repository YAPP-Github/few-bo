import { Module } from '@nestjs/common';
import { WorkbookService } from './workbook.service';
import { WorkbookController } from './workbook.controller';

@Module({
  controllers: [WorkbookController],
  providers: [WorkbookService],
})
export class WorkbookModule {}
