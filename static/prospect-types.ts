/** Canonical prospect record (API JSON uses snake_case; this file uses camelCase). */

export type LeadTier = "A" | "B" | "C" | "D";

export interface Prospect {
  id: string;
  createdAt: string;
  updatedAt: string;
  archivedAt: string | null;
  company: string;
  contactName: string;
  officeManager: string;
  phone: string;
  altPhone: string | null;
  email: string;
  street: string;
  city: string;
  state: string;
  zip: string;
  leadTier: LeadTier;
  leadScore: number | null;
  scoreReasons: string;
  signal: string;
  signalDate: string | null;
  nowOpenOrMoved: string;
  category: string;
  propertyType: string;
  hygieneFocus: string;
  website: string;
  county: string;
  providersListed: string;
  source: string;
  sourceFile: string;
  propertyVerdict: string;
  residentialCheck: string;
  remoteOrMobile: string;
  sharedAddress: boolean | null;
  suiteInAddress: boolean | null;
  daysSinceSignal?: number | null;
  status: string;
  scheduledUntil: string | null;
  timezone: string;
  transcript: TranscriptLine[];
  callLog: CallLogEntry[];
}

export interface TranscriptLine {
  id: string;
  timestamp: string;
  speaker: "Agent" | "Prospect";
  text: string;
}

export interface CallLogEntry {
  id: string;
  startedAt: string;
  endedAt: string;
  callerId: string;
  answeredBy: string;
  durationSeconds: number;
  transcriptLines: number;
  connected: boolean | null;
  outcome: string | null;
}