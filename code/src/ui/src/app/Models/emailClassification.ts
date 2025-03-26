export interface Classification{
    PrimaryAsk: string;
    SecondaryAsk: string;
    KeyElements: [];
    reasoning: string;
    Request: ClassificationResponse[];
    email_subject: string;
}

export interface ClassificationResponse{
    request_type: string;
    request_subtype: string;
    confidence_score: number;
}

export interface ClassifiedEmailResponse {
  message_id: string;
  subject: string;
  from: string;
  to: string;
  date: string;
  body: string;
  classification: Classification;
}