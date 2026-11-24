---
title: Bank transfers now match to invoices on their own
excerpt: We read the reference on each incoming transfer and mark the right invoice paid.
author: hana
category: product
date: 2026-10-21
readTime: 3
slug: bank-transfer-matching
visual: transfers
---
If you take payment by bank transfer, someone has to connect each incoming amount to the invoice it pays. That used to mean opening the bank statement, finding the line, and marking the invoice paid by hand. Plastc now does the first two steps for you.

## How matching works

Every invoice has a payment reference, such as `INV-0189`. When a transfer arrives with that reference, we compare the amount and the reference to your open invoices. If both agree, the invoice is marked paid and the transfer appears on its timeline.

If the reference is missing or mistyped, we look for an open invoice from the same customer with the same amount. When there is exactly one, we match it. When there are several, or none, we leave the transfer in **Waiting** and ask you to choose.

## What you will see

A new **Transfers** list under Payments shows each incoming transfer, the invoice it was matched to, and its status. *Matched* means the invoice is paid. *Waiting* means we could not decide on our own.

## Partial and combined payments

A transfer for less than the invoice total is recorded as a partial payment and the balance stays open. A transfer that covers two invoices is not split automatically. It waits for you, because guessing wrong would mark the wrong invoice paid.

Matching is on for every account that has a bank connection. You can turn it off in **Settings**, under Payments.
