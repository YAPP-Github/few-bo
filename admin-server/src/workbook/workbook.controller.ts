import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { WorkbookService } from './workbook.service';
import { CreateWorkbookDto } from './dto/create-workbook.dto';
import { UpdateWorkbookDto } from './dto/update-workbook.dto';

@Controller('workbook')
export class WorkbookController {
  constructor(private readonly workbookService: WorkbookService) {}

  @Post()
  create(@Body() createWorkbookDto: CreateWorkbookDto) {
    return this.workbookService.create(createWorkbookDto);
  }

  @Get()
  findAll() {
    return this.workbookService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.workbookService.findOne(+id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateWorkbookDto: UpdateWorkbookDto) {
    return this.workbookService.update(+id, updateWorkbookDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.workbookService.remove(+id);
  }
}
