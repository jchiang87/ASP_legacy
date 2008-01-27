/**
 * @file RootNTupleBase.cxx
 * @brief Provide fast vector access to columns in a ROOT ntuple.
 *
 * @author J. Chiang
 * 
 * $Header$
 */

#include <climits>

#include <iostream>
#include <stdexcept>

#include "TFile.h"
#include "TTree.h"
#include "TLeaf.h" 
#include "TObjArray.h"
#include "TObject.h"
#include "TEventList.h"

#include "grbASP/RootNTupleBase.h"

namespace grbASP {

RootNTupleBase::RootNTupleBase(const std::string & rootFile,
                               const std::string & treeName)
   : m_rootFile(TFile::Open(rootFile.c_str())), 
     m_tree((TTree *)(m_rootFile->Get(treeName.c_str()))) {
   readLeafNames();
   readLeafTypes();
}

const std::vector<double> & 
RootNTupleBase::operator[](const std::string & leafName) const {
   std::map<std::string, std::vector<double> >::const_iterator item
      = m_columns.find(leafName);
   if (item == m_columns.end()) {
      throw std::runtime_error("leaf named " + leafName + " not found.");
   }
   return item->second;      
}

const std::string & RootNTupleBase::leafType(const std::string & name) const {
   std::map<std::string, std::string>::const_iterator item 
      = m_leafTypes.find(name);
   
   if (item == m_leafTypes.end()) {
      throw std::runtime_error("leaf named " + name + " not found.");
   }
   return item->second;      
}

void RootNTupleBase::readLeafNames() {
   std::vector<TObject *> branches;

   TObjArray * branchList(m_tree->GetListOfBranches());
   size_t ncols(branchList->GetEntries());
   
   for (size_t i(0); i < ncols; i++) {
      branches.push_back(branchList->At(i));
      m_leafNames.push_back(branches[i]->GetName());
   }
}

void RootNTupleBase::readLeafTypes() {
   m_leafTypes.clear();
   TObjArray * leaves(m_tree->GetListOfLeaves());
   if (!leaves) {
      return;
   }
   UInt_t numLeaves(leaves->GetEntries());

   for (UInt_t iLeaf(0); iLeaf < numLeaves; iLeaf++) {
      std::string name(m_leafNames.at(iLeaf));
      m_leafTypes[name] = 
         std::string(((TLeaf*)leaves->At(iLeaf))->GetTypeName());
   }
}

void RootNTupleBase::readTree(const std::vector<std::string> & colNames,
                              const std::string & filterString) {
   
// Allocate space for row data.  Double_t should be sufficent.
   size_t ncols(colNames.size());
   Double_t * values(new Double_t[ncols]);
   
// Set branch addresses for each column name.
   for (size_t i(0) ; i < ncols; i++) {
      std::string name(colNames.at(i));
      if (m_leafTypes[name] == "Float_t") {
         Float_t * address = reinterpret_cast<Float_t *>(values + i);
         m_tree->SetBranchAddress(name.c_str(), address);
      } else if (m_leafTypes[name] == "Double_t") {
         Double_t * address = values + i;
         m_tree->SetBranchAddress(name.c_str(), address);
      } else if (m_leafTypes[name] == "UInt_t") {
         UInt_t * address = reinterpret_cast<UInt_t *>(values + i);
         m_tree->SetBranchAddress(name.c_str(), address);
      } else if (m_leafTypes[name] == "Int_t") {
         Int_t * address = reinterpret_cast<Int_t *>(values + i);
         m_tree->SetBranchAddress(name.c_str(), address);
      }
      m_columns[name] = std::vector<double>(0);
   }

// Apply the filterString cut.
   m_tree->Draw(">>eventList", filterString.c_str(), "", INT_MAX, 0);
   TEventList * eventList = (TEventList *)(gDirectory->Get("eventList"));
   size_t nrows(eventList->GetN());
   for (size_t j(0); j < nrows; j++) {
      m_tree->GetEntry(eventList->GetEntry(j));
      for (size_t i(0); i < ncols; i++) {
         std::string name(colNames.at(i));
         if (m_leafTypes[name] == "Float_t") {
            Float_t * value = reinterpret_cast<Float_t *>(values + i);
            m_columns[name].push_back(*value);
         } else if (m_leafTypes[name] == "Double_t") {
            Double_t * value = values + i;
            m_columns[name].push_back(*value);
         } else if (m_leafTypes[name] == "UInt_t") {
            UInt_t * value = reinterpret_cast<UInt_t *>(values + i);
            m_columns[name].push_back(*value);
         } else if (m_leafTypes[name] == "Int_t") {
            Int_t * value = reinterpret_cast<Int_t *>(values + i);
            m_columns[name].push_back(*value);
         }
      }
   }
   delete eventList;
   delete [] values;
}

} // namespace grbASP
