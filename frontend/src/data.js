import { Pill, GraduationCap, NotebookPen, StickyNote } from 'lucide-react';

export const CATEGORIES = [
  { id: 'prescription', label: 'Prescription', icon: Pill, hint: 'Diagnosed condition', desc: 'Drug names and dosages, parsed into structured fields.' },
  { id: 'exam', label: 'Exam paper', icon: GraduationCap, hint: 'Subject', desc: 'Question numbers matched to answers, subject-aware.' },
  { id: 'notes', label: 'Class notes', icon: NotebookPen, hint: 'Topic', desc: 'Lecture shorthand and terminology, kept intact.' },
  { id: 'general', label: 'General note', icon: StickyNote, hint: 'Context (optional)', desc: 'Anything else — letters, lists, reminders.' },
];

export const HISTORY_DOCS = [
  { id: 1, title: 'Dr. Reyes — follow-up script', category: 'Prescription', catId: 'prescription', date: 'Jul 8, 2026', confidence: 88 },
  { id: 2, title: 'Organic Chemistry — Midterm 2', category: 'Exam paper', catId: 'exam', date: 'Jul 6, 2026', confidence: 95 },
  { id: 3, title: 'Cardiology rotation — day 3', category: 'Class notes', catId: 'notes', date: 'Jul 3, 2026', confidence: 91 },
  { id: 4, title: 'Pediatric dosage note', category: 'Prescription', catId: 'prescription', date: 'Jun 29, 2026', confidence: 76 },
  { id: 5, title: 'Grocery + errands', category: 'General note', catId: 'general', date: 'Jun 27, 2026', confidence: 98 },
  { id: 6, title: 'Microeconomics — final', category: 'Exam paper', catId: 'exam', date: 'Jun 21, 2026', confidence: 90 },
];

// Array items can be a plain string, or [text, isLowConfidence] for flagged words
export const TRANSCRIPT_TOKENS = [
  'Pt', 'reports', 'improved', 'symptoms', 'since', 'last', 'visit.', 'Continue',
  ['Amoxicillin', true], '500mg', '—', 'three', 'times', 'daily', 'for', ['seven', true], 'more', 'days.',
  'Recheck', ['throat', true], 'culture', 'if', 'fever', 'persists', 'beyond', '72', 'hours.', 'Follow', 'up',
  'in', 'clinic', 'next', 'week', 'or', 'sooner', 'if', 'symptoms', 'worsen.',
];
