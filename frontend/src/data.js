import { Pill, GraduationCap, NotebookPen, StickyNote } from 'lucide-react';

export const CATEGORIES = [
  { id: 'prescription', label: 'Prescription', icon: Pill, hint: 'Diagnosed condition', desc: 'Drug names and dosages, parsed into structured fields.' },
  { id: 'exam', label: 'Exam paper', icon: GraduationCap, hint: 'Subject', desc: 'Question numbers matched to answers, subject-aware.' },
  { id: 'notes', label: 'Class notes', icon: NotebookPen, hint: 'Topic', desc: 'Lecture shorthand and terminology, kept intact.' },
  { id: 'general', label: 'General note', icon: StickyNote, hint: 'Context (optional)', desc: 'Anything else — letters, lists, reminders.' },
];

