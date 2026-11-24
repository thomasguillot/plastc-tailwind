import type { IconName } from '../lib/icons';

export interface Invoice {
  id: string;
  name: string;
  initials: string;
  date: string;
  status: string;
  lamp: string;
  amount: number;
}

export const CUSTOMERS: Invoice[] = [
  { id: 'INV-0193', name: 'Halden Studio', initials: 'HS', date: 'Oct 28, 2026', status: 'Paid', lamp: 'ok', amount: 4820.0 },
  { id: 'INV-0192', name: 'Ortiz & Lane', initials: 'OL', date: 'Oct 27, 2026', status: 'Paid', lamp: 'ok', amount: 1240.5 },
  { id: 'INV-0191', name: 'Northwind Co-op', initials: 'NC', date: 'Oct 12, 2026', status: 'Overdue', lamp: 'danger', amount: 9300.0 },
  { id: 'INV-0190', name: 'Priya Nair', initials: 'PN', date: 'Oct 09, 2026', status: 'Open', lamp: 'warn', amount: 612.0 },
  { id: 'INV-0189', name: 'Brightwater Labs', initials: 'BL', date: 'Oct 04, 2026', status: 'Paid', lamp: 'ok', amount: 2275.0 },
  { id: 'INV-0188', name: 'Fenwick & Daughters', initials: 'FD', date: 'Sep 30, 2026', status: 'Overdue', lamp: 'danger', amount: 3140.0 },
  { id: 'INV-0187', name: 'Tamsin Reyes', initials: 'TR', date: 'Sep 26, 2026', status: 'Paid', lamp: 'ok', amount: 860.0 },
  { id: 'INV-0186', name: 'Kettle Hill Bakery', initials: 'KH', date: 'Sep 21, 2026', status: 'Open', lamp: 'warn', amount: 415.25 },
  { id: 'INV-0185', name: 'Alder Robotics', initials: 'AR', date: 'Sep 18, 2026', status: 'Paid', lamp: 'ok', amount: 12600.0 },
  { id: 'INV-0184', name: 'Juno Park', initials: 'JP', date: 'Sep 11, 2026', status: 'Open', lamp: 'warn', amount: 1980.0 },
];

export interface Client {
  name: string;
  initials: string;
  email: string;
  count: number;
  owed: number;
  billed: number;
  last: string;
  group: string;
}

export const CLIENTS: Client[] = [
  { name: 'Halden Studio', initials: 'HS', email: 'billing@halden.studio', count: 24, owed: 0, billed: 64180, last: 'Oct 28', group: 'paid' },
  { name: 'Ortiz & Lane', initials: 'OL', email: 'accounts@ortizlane.com', count: 15, owed: 0, billed: 31480.5, last: 'Oct 27', group: 'paid' },
  { name: 'Northwind Co-op', initials: 'NC', email: 'finance@northwind.coop', count: 19, owed: 9300, billed: 71250, last: 'Oct 12', group: 'owes overdue' },
  { name: 'Priya Nair', initials: 'PN', email: 'priya@nair.design', count: 10, owed: 612, billed: 14210, last: 'Oct 9', group: 'owes' },
  { name: 'Brightwater Labs', initials: 'BL', email: 'ap@brightwater.io', count: 18, owed: 0, billed: 52300, last: 'Oct 4', group: 'paid' },
  { name: 'Fenwick & Daughters', initials: 'FD', email: 'office@fenwick.co', count: 12, owed: 3140, billed: 18900, last: 'Sep 30', group: 'owes overdue' },
  { name: 'Tamsin Reyes', initials: 'TR', email: 'tamsin@reyes.studio', count: 9, owed: 0, billed: 12600, last: 'Sep 26', group: 'paid' },
  { name: 'Kettle Hill Bakery', initials: 'KH', email: 'orders@kettlehill.co', count: 11, owed: 415.25, billed: 11449.5, last: 'Sep 21', group: 'owes' },
  { name: 'Alder Robotics', initials: 'AR', email: 'ap@alder-robotics.com', count: 22, owed: 0, billed: 96400, last: 'Sep 18', group: 'paid' },
  { name: 'Juno Park', initials: 'JP', email: 'juno@junopark.co', count: 11, owed: 1980, billed: 15840, last: 'Sep 11', group: 'owes' },
];

export interface Product {
  name: string;
  unit: string;
  price: number;
  used: number;
  group: 'active' | 'archived';
}

export const PRODUCTS: Product[] = [
  { name: 'Brand identity', unit: 'Project', price: 6400, used: 9, group: 'active' },
  { name: 'Website design', unit: 'Project', price: 8200, used: 6, group: 'active' },
  { name: 'Design day', unit: 'Day', price: 950, used: 31, group: 'active' },
  { name: 'Consulting', unit: 'Hour', price: 140, used: 64, group: 'active' },
  { name: 'Print production', unit: 'Item', price: 380, used: 12, group: 'active' },
  { name: 'Monthly retainer', unit: 'Month', price: 1800, used: 14, group: 'active' },
  { name: 'Photography, half day', unit: 'Half day', price: 620, used: 3, group: 'archived' },
];

export const MONTHS = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'];
export const REV = [21400, 23800, 22100, 27300, 26100, 31800, 30200, 36900, 34100, 48210, 41800, 44900];
export const INVOICES_SENT = [9, 10, 9, 12, 11, 13, 12, 14, 13, 16, 14, 18];

export const STATUS_SHARE = [
  { name: 'Paid', value: 62, lamp: 'lamp-ok' },
  { name: 'Open', value: 21, lamp: 'lamp-warn' },
  { name: 'Overdue', value: 9, lamp: 'lamp-danger' },
  { name: 'Draft', value: 8, lamp: 'lamp-off' },
];
export const STATUS_SHARE_LABEL = 'Invoiced this quarter: $63,800. Paid 62%, open 21%, overdue 9%, draft 8%.';

export const NAV: { key: string; label: string; icon: IconName }[] = [
  { key: 'dashboard', label: 'Dashboard', icon: 'home' },
  { key: 'invoices', label: 'Invoices', icon: 'file' },
  { key: 'customers', label: 'Customers', icon: 'users' },
  { key: 'reports', label: 'Reports', icon: 'chart' },
  { key: 'products', label: 'Products', icon: 'box' },
];

export function money(v: number, cents = true) {
  return '$' + v.toLocaleString('en-US', { minimumFractionDigits: cents ? 2 : 0, maximumFractionDigits: cents ? 2 : 0 });
}
