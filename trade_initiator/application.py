#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
import quickfix as fix
import quickfix44 as fixnn
import time
import logging
from datetime import datetime

from model.logger import setup_logger
__SOH__ = chr(1)

# Logger
setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    """FIX Application"""
    execID = 0

    def onCreate(self, sessionID):
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        print("logon successful")
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        
        if msgType.getValue() == fix.MsgType_Logon:
            message.setField(fix.EncryptMethod(0))
            message.setField(fix.HeartBtInt(30))
            print(fix.ResetSeqNumFlag(True))
            message.setField(fix.ResetSeqNumFlag(True))
            message.setField(fix.Password("rI383@l"))
            
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Admin) S >> %s" % msg)
        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Admin) R << %s" % msg)
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(App) S >> %s" % msg)
        return

    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
         # Get incoming message Type
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        msgType = msgType.getValue()

        if msgType == fix.MsgType_MarketDataRequestReject:
            text = message.getField(58)
            md_req_id = message.getField(fix.MDReqID()).getString()

            logger.warning('Market Data Request with ID %s rejected: %s', md_req_id, text)
            if self.active_subscriptions.get(md_req_id):
                print(self.active_subscriptions)
                del self.active_subscriptions[md_req_id]


    def genExecID(self):
    	self.execID += 1
    	return str(self.execID).zfill(5)

    # def put_new_order(self):
    #     """Request sample new order single"""
    #     message = fix.Message()
    #     header = message.getHeader()

    #     header.setField(fix.MsgType(fix.MsgType_NewOrderSingle)) #39 = D 

    #     message.setField(fix.ClOrdID(self.genExecID())) #11 = Unique Sequence Number
    #     message.setField(fix.Side(fix.Side_BUY)) #43 = 1 BUY 
    #     message.setField(fix.Symbol("MSFT")) #55 = MSFT
    #     message.setField(fix.OrderQty(10000)) #38 = 1000
    #     message.setField(fix.Price(100))
    #     message.setField(fix.OrdType(fix.OrdType_LIMIT)) #40=2 Limit Order 
    #     message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION)) #21 = 3
    #     message.setField(fix.TimeInForce('0'))
    #     message.setField(fix.Text("NewOrderSingle"))
    #     trstime = fix.TransactTime()
    #     trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
    #     message.setField(trstime)

    #     fix.Session.sendToTarget(message, self.sessionID)

    def create_new_order(self):
        pass

    def run(self):
        """Run"""
        while 1:
            options = str(input("Please choose 1 for market order creation or 2 for Exit!\n"))
            if options == '1':
                self.create_new_order()
                print("Done: Get Market Data\n")
                continue
            if  options == '2':
                sys.exit(0)
            else:
                print("Valid input is 1 for order, 2 for exit\n")
            time.sleep(2)
